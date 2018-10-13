from django.conf.urls import url

from views import AddScreen, ReserveTickets, GetAvailableSeats

urlpatterns = [
    url(r'^$', AddScreen.as_view()),
    url(r'^(?P<screenName>\w+)/reserve$', ReserveTickets.as_view()),
    url(r'^(?P<screenName>\w+)/seats', GetAvailableSeats.as_view()),
]