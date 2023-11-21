from django.urls import path
from myEventsApp import views


app_name = 'myEventsApp'
urlpatterns = [
                  # event views
                  path('', views.home, name="home"),
                  path('events/', views.events_list, name='events_list'),
                  path('events/sorted', views.sorted_events_list, name='sorted-events_list'),
                  path('edit-event/<int:event_id>/', views.edit_event, name="edit_event"),
                  path('delete-event/<int:event_id>/', views.delete_event_confirm, name='delete_event_confirm'),
                  path('create-event/', views.create_event, name="create_event"),
                  path('events/<int:event_id>/', views.event_details, name='event_details'),
                  path('events/attend', views.attend_event, name='attend-event'),
                  path('events/calendar-display', views.calendar_display, name='calendar_display'),
                  path('events/comment', views.add_comment, name="add-comment"),
                  path('events/comment/edit/<int:comment_id>', views.edit_comment, name="edit-comment"),
                  path('events/comment/delete', views.delete_comment, name="delete-comment"),
              ]
