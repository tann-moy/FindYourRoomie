from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.shortcuts import render
from .models import Room


def room_list(request):
    rooms = Room.objects.all().order_by('-created_at')

    # Search by location
    location = request.GET.get('location')
    if location:
        rooms = rooms.filter(location__icontains=location)

    # Filter by maximum rent
    max_rent = request.GET.get('max_rent')
    if max_rent:
        rooms = rooms.filter(rent__lte=max_rent)

    # Filter by room type
    room_type = request.GET.get('room_type')
    if room_type:
        rooms = rooms.filter(room_type=room_type)

    context = {
        'rooms': rooms,
    }

    return render(request, 'properties/room_list.html', context)

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .form import RoomForm
from .models import Room


@login_required
def room_create(request):

    if request.method == 'POST':
        form = RoomForm(request.POST)

        if form.is_valid():
            room = form.save(commit=False)

            # Assign the logged-in user as room owner
            room.owner = request.user

            room.save()

            # Save selected amenities
            form.save_m2m()

            return redirect('properties:room_list')

    else:
        form = RoomForm()

    context = {
        'form': form
    }

    return render(request, 'properties/room_form.html', context)
@login_required
def room_delete(request, pk):

    room = get_object_or_404(
        Room,
        pk=pk,
        owner=request.user
    )

    if request.method == 'POST':
        room.delete()
        return redirect('properties:room_list')

    return render(
        request,
        'properties/room_conform_delete.html',
        {'room': room}
    )

@login_required
def room_update(request, pk):

    # Find the room belonging to the logged-in owner
    room = get_object_or_404(
        Room,
        pk=pk,
        owner=request.user
    )

    if request.method == 'POST':

        form = RoomForm(request.POST, instance=room)

        if form.is_valid():

            form.save()

            return redirect('properties:room_list')

    else:

        form = RoomForm(instance=room)

    context = {
        'form': form,
        'room': room,
    }

    return render(request, 'properties/room_form.html', context)
