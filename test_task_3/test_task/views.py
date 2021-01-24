from django.views.generic.list import ListView
from django.views.generic.edit import FormMixin

from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from .forms import SelectDateForm, SubmitForm
from .models import Table, Booking, Visitor
from .serializers import TableSerializer
from .local_settings import *

from datetime import date, datetime
from dateutil.relativedelta import *

from email.mime.multipart import MIMEMultipart
from django.template.loader import render_to_string
from email.mime.text import MIMEText
from smtplib import SMTP


class MainPageView(FormMixin, ListView):
    model = Table
    template_name = 'index.html'
    context_object_name = 'tables'
    form_class = SelectDateForm
    queryset = Table.objects.all()
    email_template = 'booking.html'

    def check_buttons(self, context, date_to_filter):
        date_to_filter = datetime.strptime(str(date_to_filter), '%Y-%m-%d')
        if self.request.POST.get('previous'):
            context['form'] = SelectDateForm(initial={'date': date_to_filter - relativedelta(days=1)})
            return context, date_to_filter - relativedelta(days=1)
        if self.request.POST.get('next'):
            context['form'] = SelectDateForm(initial={'date': date_to_filter + relativedelta(days=1)})
            return context, date_to_filter + relativedelta(days=1)
        if self.request.POST.get('current'):
            context['form'] = SelectDateForm(initial={'date': date.today()})
            return context, date.today()
        return context, date_to_filter


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date_to_filter = self.request.POST.get('date') if self.request.POST.get('date') else date.today()
        context, date_to_filter = self.check_buttons(context, date_to_filter)
        booked_tables = Booking.objects.filter(date=date_to_filter)
        context['booked'] = [table.table for table in booked_tables]
        context['submit_form'] = SubmitForm()
        return context

    def send_email(self, bookings):
        msg = MIMEMultipart('alternative') # this is the special format for email messages
        msg['Subject'] = f'Table ordering'
        msg['From'] = 'Interesting candidate Nikita'
        msg['To'] = bookings[0].visitor.name
        html = self.email_template
        html = render_to_string(html, {'bookings': bookings, 'visitor': bookings[0].visitor, 'date': bookings[0].date})
        part2 = MIMEText(html, 'html') # inserting html into a mail
        msg.attach(part2)
        """ SMTP connection is more secure than django default send_mail """
        server = SMTP(EMAIL_SERVER, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SERVER, bookings[0].visitor.email if bookings[0].visitor.email else None, msg.as_string())
        server.quit()

    def post(self, request, *args, **kwargs):
        if self.request.POST.get('request') == 'Book':
            bookings = []
            visitor = Visitor.objects.get_or_create(name=self.request.POST.get('name'),
                                                    email=self.request.POST.get('email'))[0]
            for table in [int(table) for table in self.request.POST['tables'].split(',')]:
                booking = Booking.objects.create(table_id=table, visitor=visitor, date=self.request.POST.get('date'))
                bookings.append(booking)
            self.send_email(bookings)
        return super().get(request, *args, **kwargs)
