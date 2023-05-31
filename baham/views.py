from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.template import loader
from django.urls import reverse
from baham.enum_types import VehicleType
from baham.models import VehicleModel
# Create your views here.
def view_home (request):
    
    template = loader.get_template('home.html')
    context = {
    'navbar': 'home',
    }
    return HttpResponse (template.render(context, request))

def view_aboutus (request):
    template = loader.get_template('aboutus.html')
    context = {
    'navbar': 'aboutus',
    }
    return HttpResponse (template.render(context, request))
def view_vehicles (request):
    template = loader.get_template('vehicles.html')
    vehicles = VehicleModel.objects.get(voided=False).order_by('vendor')
    context = {
    'navbar': 'vehicles',
    'vehicles': vehicles
    }
    return HttpResponse (template.render(context, request))

def create_vehicle (request):
    template = loader.get_template('createvehicle.html')
    context = {
    'navbar': 'vehicles',
    'vehicle_types': [(t.name, t.value) for t in VehicleType]
    }
    return HttpResponse (template.render(context, request))

def save_vehicle(request):
    _registration_number = request.POST.get('registration_number')
    exists = Vehicle.objects.filter(registration_number=_registration_number)
    if exists:
        return render_create_vehicle(request, message="Another vehicle with this registration number already exists.")
    _model_uuid = request.POST.get('model_uuid')
    _model = VehicleModel.objects.filter(uuid=_model_uuid).first()
    if not _model:
        return render_create_vehicle(request, message="Selected Vehicle model not found! Please select from given list only.")
    _colour = request.POST.get('colour')
    if not validate_colour(_colour):
        return render_create_vehicle(request, message="Invalid colour code!")    
    _status = request.POST.get('status')
    print (_status)
    _picture1 = request.FILES.get('image1')
    _picture2 = request.FILES.get('image2')
    vehicle = Vehicle.objects.create(registration_number=_registration_number, colour=_colour, model=_model, 
                                     owner=request.user, status=_status, picture1=_picture1, picture2=_picture2)
    vehicle.save()
    return HttpResponseRedirect(reverse('vehicles'))

#activity-3
def delete_vehicle_model(request):
    vehicleModel = VehicleModel (vendor=_vendor, model=_model, type=_type, capacity=_capacity)
    vehicleModel.void()
    
def delete_vehicle_model(request):
    vehicleModel = VehicleModel (vendor=_vendor, model=_model, type=_type, capacity=_capacity)
    vehicleModel.unvoid()def edit_vehicle(request, uuid):
    template = loader.get_template('editvehicle.html')
    vehicle_model = VehicleModel.objects.filter(uuid=uuid).first()
    if not vehicle_model:
        return HttpResponseBadRequest('This object does not exit!')
    context = {
        'navbar': 'vehicles',
        'is_superuser': request.user.is_superuser,
        'vehicle_types': [(t.name, t.value) for t in VehicleType],
        'vehicle': vehicle_model
    }
    return HttpResponse(template.render(context, request))


def update_vehicle(request):
    _uuid = request.POST.get('uuid')
    _vendor = request.POST.get('vendor')
    _model = request.POST.get('model')
    _type = request.POST.get('type')
    _capacity = int(request.POST.get('capacity'))
    if not _vendor or not _model:
        return HttpResponseBadRequest('Manufacturer and Model name fields are mandatory!')
    if not _capacity or _capacity < 2:
        _capacity = 2 if _type == VehicleType.MOTORCYCLE else 4
    vehicle_model = VehicleModel.objects.filter(uuid=_uuid).first()
    if not vehicle_model:
        return HttpResponseBadRequest('Requested object does not exist!')
    vehicle_model.vendor = _vendor
    vehicle_model.model = _model
    vehicle_model.type = _type
    vehicle_model.capacity = _capacity
    vehicle_model.update(update_by=request.user)
    return HttpResponseRedirect(reverse('vehicles'))

#############
### REST ####
#############
def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrf_token': csrf_token})


def get_all_vehicle_models(request):
    if request.method == 'GET':
        vehicle_models = VehicleModel.objects.all()
        data = []
        for model in vehicle_models:
            data.append({
                'uuid': model.uuid,
                'vendor': model.vendor,
                'model': model.model,
                'type': model.type,
                'date_created': model.date_created,
                'created_by': str(model.created_by),
            })
        return JsonResponse({'results': data})
    else:
        return JsonResponse({'error': 'Invalid endpoint or method type'}, status=400)


def get_vehicle_model(request, uuid):
    if request.method == 'GET':
        model = VehicleModel.objects.filter(uuid=uuid).first()
        data = {
            'uuid': model.uuid,
            'vendor': model.vendor,
            'model': model.model,
            'type': model.type,
            'capacity': model.capacity,
            'date_created': model.date_created,
            'created_by': str(model.created_by),
            'date_updated': model.date_updated,
            'updated_by': str(model.updated_by),
            'voided': model.voided,
            'date_voided': model.date_voided,
            'voided_by': str(model.voided_by),
            'void_reason': model.void_reason,
        }
        return JsonResponse({'results': data})
    else:
        return JsonResponse({'error': 'Invalid endpoint or method type'}, status=400)


def create_vehicle_model(request):
    if request.method == 'POST':
        _vendor = request.POST.get('vendor')
        _model = request.POST.get('model')
        _type = request.POST.get('type')
        _capacity = request.POST.get('capacity')
        vehicle_model = VehicleModel.objects.create(vendor=_vendor, model=_model, type=_type, capacity=_capacity)
        response_data = {
            'message': 'Vehicle model created successfully',
            'uuid': vehicle_model.uuid,
        }
        return JsonResponse(response_data, status=201)
    else:
        return JsonResponse({'error': 'Invalid endpoint or method type'}, status=400)


def update_vehicle_model(request, uuid):
    if request.method == 'PUT':
        params = QueryDict(request.body)
        _vendor = params.get('vendor')
        _model = params.get('model')
        _type = params.get('type')
        _capacity = params.get('capacity')
        vehicle_model = VehicleModel.objects.filter(uuid=uuid).first()
        if not vehicle_model:
            response_data = {
                'error': 'Vehicle model not found',
            }
            return JsonResponse(response_data, status=404)
        vehicle_model.vendor = _vendor
        vehicle_model.model = _model
        vehicle_model.type = _type
        vehicle_model.capacity = _capacity
        vehicle_model.update()
        response_data = {
            'message': 'Vehicle model updated successfully',
            'uuid': vehicle_model.uuid,
        }
        return JsonResponse(response_data, status=200)
    else:
        return JsonResponse({'error': 'Invalid endpoint or method type'}, status=400)


def delete_vehicle_model(request, uuid):
    if request.method == 'DELETE':
        vehicle_model = VehicleModel.objects.filter(uuid=uuid).first()
        if not vehicle_model:
            response_data = {
                'error': 'Vehicle model not found',
            }
            return JsonResponse(response_data, status=404)
        vehicle_model.delete()
        response_data = {
            'message': 'Vehicle model voided successfully'
        }
        return JsonResponse(response_data, status=200)
    else:
        return JsonResponse({'error': 'Invalid endpoint or method type'}, status=400)



        def get_all_user_profiles(request):
    if request.method == 'GET':
        users = UserProfile.objects.filter(voided=False)
        if users:
            data = []
            for user in users:
                data.append({
                    'uuid': str(user.uuid),
                    'birthdate': user.birthdate,
                    'gender': user.gender,
                    'type': user.type,
                    'primary_contact': user.primary_contact,
                    'address': user.address,
                    'town': user.town,
                    'bio': user.bio,
                    'date_created': user.date_created,
                    'created_by': str(user.created_by),
                })
            return JsonResponse({"results": data}, status=200)
        else:
            return JsonResponse({'error': 'User Profiles Not Found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid endpoint or method type'}, status=400)


def get_user_profile(request, uuid):
    if request.method == 'GET':
        user_model = UserProfile.objects.filter(uuid=uuid, voided=False).first()
        if user_model:
            data = {
                'uuid': str(user_model.uuid),
                'birthdate': user_model.birthdate,
                'gender': user_model.gender,
                'type': user_model.type,
                'primary_contact': user_model.primary_contact,
                'address': user_model.address,
                'town': user_model.town,
                'bio': user_model.bio,
                'date_created': user_model.date_created,
                'created_by': str(user_model.created_by),
            }
            return JsonResponse({'results': data}, status=200)
        else:
            return JsonResponse({'error': 'User Profile Not Found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid endpoint or method type'}, status=400)


def create_user_profile(request):
    if request.method == 'POST':
        _username = request.POST.get('username')
        _pass = request.POST.get('pass')
        _birthdate = request.POST.get('birthdate')
        _gender = request.POST.get('gender')
        _type = request.POST.get('type')
        _primary_contact = request.POST.get('primary_contact')
        _alternate_contact = request.POST.get('alternate_contact')
        _address = request.POST.get('address')
        _address_latitude = request.POST.get('address_latitude')
        _address_longitude = request.POST.get('address_longitude')
        _landmark = request.POST.get('landmark')
        _town = request.POST.get('town')
        _active = request.POST.get('active')
        _bio = request.POST.get('bio')

        user_profile = UserProfile.objects.create(
            user=User.objects.create_user(username=_username, password=_pass),
            birthdate=_birthdate,
            gender=_gender,
            type=_type,
            primary_contact=_primary_contact,
            alternate_contact=_alternate_contact,
            address=_address,
            address_latitude=_address_latitude,
            address_longitude=_address_longitude,
            landmark=_landmark,
            town=_town,
            active=_active,
            bio=_bio,
        )

        response_data = {
            'message': 'User profile created successfully',
            'uuid': str(user_profile.uuid),
        }
        return JsonResponse(response_data, status=201)
    else:
        return JsonResponse({'error': 'Invalid endpoint or method type'}, status=400)


def update_user_profile(request, uuid):
    if request.method == 'PUT':
        params = QueryDict(request.body)
        _type = params.get('type')
        _primary_contact = params.get('primary_contact')
        _alternate_contact = params.get('alternate_contact')
        _address = params.get('address')
        _address_latitude = params.get('address_latitude')
        _address_longitude = params.get('address_longitude')
        _landmark = params.get('landmark')
        _town = params.get('town')
        _active = params.get('active')
        user_profile = UserProfile.objects.filter(uuid=uuid, voided=False).first()
        if not user_profile:
            response_data = {
                'error': 'User profile not found',
            }
            return JsonResponse(response_data, status=404)
        user_profile.type = _type
        user_profile.primary_contact = _primary_contact
        user_profile.alternate_contact = _alternate_contact
        user_profile.address = _address
        user_profile.address_latitude = _address_latitude
        user_profile.address_longitude = _address_longitude
        user_profile.landmark = _landmark
        user_profile.town = _town
        user_profile.active = _active

        user_profile.save()
        response_data = {
            'message': 'User profile updated successfully',
            'uuid': str(user_profile.uuid),
        }
        return JsonResponse({"results": response_data}, status=200)
    else:
        return JsonResponse({'error': 'Invalid endpoint or method type'}, status=400)


def delete_user_profile(request, uuid):
    if request.method == 'DELETE':
        user_profile = UserProfile.objects.filter(uuid=uuid, voided=False).first()
        if not user_profile:
            response_data = {
                'error': 'User profile not found',
            }
            return JsonResponse(response_data, status=404)
        user_profile.delete()
        response_data = {
            'message': 'User profile voided successfully'
        }
        return JsonResponse(response_data, status=200)
    else:
        return JsonResponse({'error': 'Invalid endpoint or method type'}, status=400)


