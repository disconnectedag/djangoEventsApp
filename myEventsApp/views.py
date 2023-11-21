from datetime import date

from django.contrib import messages
from django.core.serializers import serialize
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from actions.models import Action
from .forms import EventForm
from .models import Event, User, Comment


# Create your views here.
def events_list(request):
    posted_events = Event.objects.all().order_by('event_date')
    return render(request, "myEventsApp/event/event-listings.html", {"events": posted_events})


def sorted_events_list(request):
    posted_events = Event.objects.all().order_by('date_posted')
    return render(request, "myEventsApp/event/event-listings.html", {"events": posted_events})


def event_details(request, event_id):
    event = Event.objects.get(pk=event_id)
    comments = event.comments.all().order_by('-time_posted')
    return render(request,
                  "myEventsApp/event/event-details.html",
                  {"event": event, 'comments': comments}
                  )


def home(request):
    if request.session.get("username", False):
        actions = Action.objects.all()

        return render(request, "myEventsApp/dashboard.html", {"actions": actions})

    return render(request, "myEventsApp/home.html")


def delete_event_confirm(request, event_id):
    # Check if the user is an admin
    if request.session.get('role') != 'admin':
        return redirect('myEventsApp:events_list')

    # Find the event by its ID
    event_to_delete = Event.objects.get(pk=event_id)

    # If the method is POST, it means the form has been submitted for deletion
    if request.method == 'POST':
        if event_to_delete:
            username = request.session.get('username')
            user = User.objects.get(username=username)
            action = Action(
                user=user,
                verb="deleted event",
                target=event_to_delete
            )
            action.save()
            event_to_delete.delete()

        messages.add_message(request, messages.WARNING,
                             "You successfully deleted the event: %s" % event_to_delete.title)
        return redirect('myEventsApp:events_list')

    return render(request, 'myEventsApp/event/delete-event.html', {'event': event_to_delete})


def create_event(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)

        if form.is_valid():
            new_event = form.save(commit=False)
            username = request.session.get('username')
            user = User.objects.get(username=username)
            new_event.user = user
            new_event.save()

            # log the action
            action = Action(
                user=user,
                verb="created event",
                target=new_event
            )
            action.save()
            messages.add_message(request, messages.SUCCESS,
                                 "You successfully submitted the event: %s" % new_event.title)
            return redirect('myEventsApp:event_details', new_event.id)
    form = EventForm
    return render(request, 'myEventsApp/event/event-add.html', {'form': form})


def edit_event(request, event_id):
    # Retrieve the event using the event_id
    event = Event.objects.get(pk=event_id)
    event.event_date = event.event_date.strftime('%Y-%m-%dT%H:%M')
    username = request.session.get('username')
    user = User.objects.get(username=username)

    if request.method == 'POST':
        # Handle form submission and update the event
        event.title = request.POST.get('title')
        event.description = request.POST.get('description')
        event.location = request.POST.get('location')
        event.event_date = request.POST.get('date_of_event')
        event.attendees = request.POST.get('attendees')
        event.address = request.POST.get('address')
        event.save()
        action = Action(
            user=user,
            verb="edited an event",
            target=event
        )
        action.save()

        # Redirect to a view displaying the updated event
        messages.add_message(request, messages.INFO, "You successfully edited the event: %s" % event.title)
        return redirect('myEventsApp:event_details', event_id=event.id)

    return render(request, 'myEventsApp/event/edit-event.html', {'event': event})


def attend_event(request):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if is_ajax and request.method == 'POST':
        event_id = request.POST.get('event_id')
        try:
            event = Event.objects.get(pk=event_id)
            event.attendees = event.attendees + 1
            event.save()
            action = Action(
                user=event.user,
                verb="attending an event",
                target=event
            )
            action.save()
            return JsonResponse({"success": "success", "attendCount": event.attendees}, status=200)
        except Event.DoesNotExist:
            return JsonResponse({"error": "No event found with that id"}, status=200)
    else:
        return JsonResponse({"error": "Invalid ajax response"}, status=400)


def add_comment(request):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax and request.method == 'POST':
        event_id = request.POST.get('event_id')
        body = request.POST.get('body')
        username = request.session.get('username')
        user = User.objects.get(username=username)
        try:
            event = Event.objects.get(pk=event_id)
            new_comment = Comment(event=event, name=username, body=body)
            new_comment.save()
            action = Action(
                user=user,
                verb="added a comment",
                target=event
            )
            action.save()
            formatted_time = new_comment.time_posted.strftime("%B %d, %Y, %I:%M %p")
            return JsonResponse({"success": "success", "name": new_comment.name, "body": new_comment.body,
                                 "time": formatted_time, "comment_id": new_comment.id}, status=200)
        except Event.DoesNotExist:
            return JsonResponse({"error": "No event found with that id"}, status=200)
    else:
        return JsonResponse({"error": "Invalid ajax response"}, status=400)


def edit_comment(request, comment_id):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    comment = Comment.objects.get(pk=comment_id)
    username = request.session.get('username')
    user = User.objects.get(username=username)
    if is_ajax and request.method == 'POST':
        comment_body = request.POST.get('comment_body')
        comment.body = comment_body
        comment.save()
        action = Action(
            user=user,
            verb="edited a comment",
            target=comment
        )
        action.save()
        redirect_url = reverse('myEventsApp:event_details', args=[comment.event_id])
        messages.add_message(request, messages.INFO, "You successfully edited the comment: %s" % comment.body)
        return JsonResponse({'message': 'Comment updated successfully', 'redirect_url': redirect_url}, status=200)
    return render(request, 'myEventsApp/comment/edit-comment.html', {"comment": comment})


def delete_comment(request):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax and request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        comment = get_object_or_404(Comment, pk=comment_id)

        username = request.session.get('username')
        user = get_object_or_404(User, username=username)
        action = Action(user=user, verb="deleted a comment", target=comment)
        action.save()
        comment.delete()
        return JsonResponse({"success": "success"}, status=200)


def calendar_display(request):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax and request.method == 'POST':
        event_day = int(request.POST.get('event_day'))
        try:
            event = Event.objects.filter(event_date__date=date(2023, 10, event_day))
            serialized_data = serialize('json', event)
            return JsonResponse({"success": "success", "filtered_events": serialized_data}, status=200)
        except Event.DoesNotExist:
            return JsonResponse({"error": "No event found with that date"}, status=200)
    else:
        return JsonResponse({"error": "Invalid ajax response"}, status=400)
