# Create your tests here.
from django.test import Test Case
from django.contrib.auth.models import User
from baham.enum_types import VehicleType
from baham.models import VehicleModel

class VehicleModelTest (TestCase):
    
    def setup(self): 
       ''''
       Provide all pre-requisites userd in the tests
        '''
    self.superuser = User.objects.create_superuser (username='admin', email='admin@dareecha.com', password='weakestPass')
    return super().setup()
    def test_auto_date_created_on_save(self):
        obj = VehicleModel.objects.create (vendor='Kia', model='Sportage', type=VehicleType. SUV, capacity=7)
        # See if the date_created is automatically set
        # Pass this test if obj.date_created is not None
        self.assertIsNotNone (obj.created_by)
        self.assertIsNotNone (obj.date_created)
    
    def test_create_with_same_vendor_and_model(self):
        # Create a new object
        kia = VehicleModel.objects.create(vendor='Kia', model='Sportage', type=VehicleType. SUV, capacity=7)
        # An error must be thrown
        with self.assertRaises (Exception):
        # Create a new object with same vendor and model
        VehicleModel.objects.create(vendor='Kia', model='Sportage', type=VehicleType. SEDAN, capacity=5)
    def test_update_with_same_vendor_and_model(self):
        VehicleModel.objects.create(vendor='Honda', model='CD125', type=VehicleType.MOTORCYCLE, capacity=2)
        cd70 = VehicleModel.objects.create (vendor='Honda', model='CD70', type=VehicleType.MOTORCYCLE, capacity=2)
        cd70.model = 'CD125'
        # An error must be thrown
         with self.assertRaises (Exception):
            # Create a new object with same vendor and model
            cd70.update()
    #1.One vehicle per Owner.    
    def test_one_vehicle_per_owner(self):
        khurram = user.objects.create(username='khurram', email='khurram@dareecha.com", password='weakestPass')
        cd70 = vehicleModel, objects.create(vendor='Honda', model='CD70', type=vehicleType.MOTORCYCLE, capacity=2)
        cd125 = VehicleModel.objects.create(vendor='Honda', model='CD125', type=VehicleType,MOTORCYCLE, capacity=2)
        Vehicle.objects.create(registration_number='KHI-885', colour='#ff0off', model-cd70, owner-khurram, status-Vehiclestatus. AVAILBLE)
        # An error must be thrown
        with self. assertRaises (Exception):
            # Create a new object with same vendor and model
            Vehicle.objects.create (registration_number='KHI-996', colour='#ffff00'; model-cd125, owner-owais, status-Vehiclestatus.AVAILBLE)
    #2.No more passengers than the vehicle’s sitting capacity.
    def test_passengers_capacity(self):
        khurram = user.objects.create(username='khurram', email='khurram@dareecha.com", password='weakestPass')
        cd70 = vehicleModel, objects.create(vendor='Honda', model='CD70', type=vehicleType.MOTORCYCLE, capacity=2)
        cd125 = VehicleModel.objects.create(vendor='Honda', model='CD125', type=VehicleType,MOTORCYCLE, capacity=2)
        Vehicle.objects.create(registration_number='KHI-885', colour='#ff0off', model-cd70, owner-khurram, status-Vehiclestatus. AVAILBLE)
         with self.assertRaises(Exception):
            Contract.objects.create(vehicle=self.vehicle, effective_start_date="2023-05-31", expiry_date="2023-06-31",
                                    fuel_share="50", maintenance_share="50",
                                    companion=self.userprofileCompanion, is_active=True)
    #3.Total share cannot exceed 100.
    def test_total_share(self):
        invalid_contract = Contract.objects.create(vehicle=self.vehicle, companion=self.userprofileCompanion,
                                                   effective_start_date="2023-05-31", expiry_date="2023-06-31",
                                                   is_active=True, fuel_share=110, maintenance_share=50)

        self.assertLessEqual(invalid_contract.fuel_share + invalid_contract.maintenance_share, 100)
    #4.Companions cannot have multiple active contracts simultaneously.
    def test_multiple_active_contracts(self):
        invalid_contract = Contract.objects.create(vehicle=self.vehicle, companion=self.userprofileCompanion,
                                                    effective_start_date="2023-05-29", expiry_date="2023-06-10",
                                                    is_active=True, fuel_share=50, maintenance_share=30)

        self.assertFalse(invalid_contract.is_active)


#RestApi
class RESTAPITest (TestCase):
    def setup(self):
        self.superuser = User.objects.create_superuser (username=USERNAME, email='admin@dareecha.com', password=PASSWORD)
        return super().setup()
    def test_get_csrf_token(self):
        credentials = f"{USERNAME}: {PASSWORD}"
        encoded_credentials = base64.b64encode (credentials.encode('utf-8')).decode('utf-8')
        response = self.client.get(reverse('get_csrf_token'), HTTP_AUTHORIZATION='Basic + encoded_credentials)
        self.assertEquals (response.status_code, 200)
        self.assertTrue (response.json())
        self.assertIsNotNone (response.json () ['csrf_token'])
    def test_get_vehicle_model_by_uuid (self):
        model = VehicleModel.objects.create(vendor='Honda', model='CD125', type=VehicleType.MOTORCYCLE, capacity=2)
        credentials f"{USERNAME}: {PASSWORD}"
        encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
        response = self.client.get (reverse('get_vehicle_model', args=[model.uuid,]), HTTP_AUTHORIZATION='Basic ' + encoded_Credentials) 
        vehicle_obj = response.json () ['results']
        self.assertEquals(str(model.uuid), vehicle_obj['uuid'])
