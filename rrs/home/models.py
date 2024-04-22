from django.db import models
from datetime import datetime,date
from  django.contrib.auth.models import AbstractUser
from django.utils.crypto  import get_random_string
import os

# Create your model

class user_master(models.Model):
    firstname=models.CharField("First Name",max_length=50)
    lastname=models.CharField("Last Name", max_length=50,blank=True)
    username = models.CharField("Username", max_length=50,unique=True)
    password = models.CharField("Password",max_length=128)
    dob=models.DateField()
    email = models.EmailField()
    mobile=models.IntegerField()
    address=models.TextField()
    regis_date=models.DateField(default=date.today())
    
    def __str__(self):
        return self.username
    class Meta:
        db_table = "user_master"
        
class station_master(models.Model):
    station_id=models.AutoField(primary_key=True)
    station_name=models.CharField(max_length=30,null=False)
    station_code=models.CharField(unique=True,max_length=5, null=False)
    location = models.CharField(max_length=50,null=False)
    zone=models.CharField(max_length=30,null=False)
    state=models.CharField(max_length=20,null=False)

    def __str__(self) :
        return self.station_name
    class Meta:
        db_table= "station_master"  # specify the table name in database if not same as ClassName  
# for feedback
class  user_feedback(models.Model):
    username=models.CharField(max_length=30)
    subject=models.CharField(max_length=100)
    message=models.TextField()
    email = models.EmailField(default=None, blank=True)

    def  __str__(self):
        return self.username + "-"+self.subject
    class Meta:
        db_table= 'user_feedback'

# for train_master model
class  train_master(models.Model):
    train_no  = models.IntegerField(primary_key=True)
    train_name = models.CharField(max_length=50, null = False)
    source_station=models.ForeignKey(station_master, related_name="source_station", on_delete=models.CASCADE,to_field="station_code", verbose_name="Source Station",null=True)
    dest_station = models.ForeignKey(station_master, on_delete=models.CASCADE, related_name='dest_station',to_field="station_code", null=True)
    depart_time = models.TimeField(null=True,blank=True,default=None)
    arrival_time=models.TimeField(null=True,blank=True, default=None)
    journey_duration=models.CharField(max_length=20)
    
    def  __str__(self):
        return  f'{self.train_name}-{self.depart_time}'
        
    class Meta:
        db_table =  'train_master'

class train_schedule(models.Model):  
    schedule_id=models.AutoField(primary_key=True,default=None)
    train_no=models.ForeignKey(train_master,on_delete=models.CASCADE)
    station_code=models.ForeignKey(station_master,on_delete=models.CASCADE,to_field= 'station_code',default=None)
    stop_time=models.TimeField(null=True,blank=True)
    depart_time=models.TimeField(null=True,blank=True)
    arrival_time=models.TimeField(null=True)
    day=models.IntegerField(default=1,null=False)
    seq=models.PositiveSmallIntegerField(null=False,default=None)
    distance=models.IntegerField(null=False,default=0)
    # def get_stop_time(self):
    #     """Returns stop time formatted as string (HH:MM)"""
    #     return str(self.stop_time).split('.')[0] 

    # def set_stop_time(self,value):
    #     """Sets stop time from a string (HH:MM)"""
    #     self.stop_time = datetime.datetime.strptime(value,"%H:%M").time()

    # stop_time = property(get_stop_time,set_stop_time)
   
    def __str__(self):
        return f'{self.train_no}-{self.station_code}'

    class Meta:
        db_table= "train_schedule"
        verbose_name="Train Schedule"
        verbose_name_plural="Trains Schedules"

    
# passenger models
class passenger_master(models.Model):
    pass_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    age = models.PositiveSmallIntegerField()
    gender = models.CharField(max_length=6)
    seat_no=models.CharField(max_length=5,default=None)
    pnr_no=models.ForeignKey('ticket_master',on_delete=models.CASCADE,default=None)
    def __str__(self):
        return self.name
    class Meta:
        db_table = "passenger_master"
    
class class_master(models.Model):
    class_id = models.IntegerField(primary_key=True)
    class_name = models.CharField(max_length=20,null=False)
    description= models.TextField(max_length=100)
    features = models.TextField(max_length=100)
    capacity = models.IntegerField()
   
    class Meta:
        db_table = "class_master"
    
    def __str__(self):
        return self.class_name

class RouteMaster(models.Model):
    route_id = models.AutoField(primary_key=True)
    source_station = models.ForeignKey('station_master', on_delete=models.CASCADE, to_field="station_code",related_name='source_routes')
    destination_station = models.ForeignKey('station_master', on_delete=models.CASCADE,to_field="station_code", related_name='destination_routes')
    distance = models.DecimalField(max_digits=10, decimal_places=2)
    route_name = models.CharField(max_length=255, blank=True, null=True)
    


    
    def __str__(self):
        return f"{self.source_station.station_name} to {self.destination_station.station_name}"
    class Meta:
        db_table = "route_master"

class routestation(models.Model):
    id = models.AutoField(primary_key=True)
    train_no = models.ForeignKey('train_master',on_delete=models.CASCADE)
    station_id = models.ForeignKey('station_Master', on_delete=models.PROTECT)
    sequence_no = models.PositiveSmallIntegerField() # Sequence number of the station in a train journey
                                                # 1 means it is the first station and so on.
    arrival_time = models.TimeField()
    departure_time = models.TimeField()

    class Meta:
        db_table="routestation"


# A Train can have multiple schedules for different days
class ScheduleMaster(models.Model):
    schedule_id = models.AutoField(primary_key=True)
    train_no = models.ForeignKey('train_master',on_delete=models.PROTECT)
    route_id = models.ForeignKey('RouteMaster',on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    # If this field is not provided then we assume that the train runs everyday from the start date till the end date.
    # If this field is not provided then we assume that it runs everyday from start date till end date.
    weekdays=[
        ("Monday", "Monday"),
        ("Tuesday","Tuesday"),
        ("Wednesday","Wednesday"),
        ("Thursday","Thursday"),
        ("Friday","Friday"),
        ("Saturday","Saturday"),
        ("Sunday","Sunday")
      ]
    week = models.CharField(max_length=9, choices=[item for item in weekdays])

    @property
    def get_weekday(self):
        if self.week == 'Monday':
            return 'Monday'
        elif self.week == 'Tuesday':
            return 'Tuesday'
        else:   
            return f"{self.week}s"
    
    def __str__(self):
        #return f"Schedule {self.schedule_id}: {self.train.name} - {self.start_date}-{self.end_date}, Week:{self.week
        return f"Schedule {self.schedule_id}: {self.train.train_name} - {self.start_date}"
# create model for coach master
class coach(models.Model):
    coach_no=models.CharField(max_length=10,unique=True)
    coach_type=models.ForeignKey('class_master',on_delete=models.CASCADE)
    capacity_passen=models.PositiveIntegerField()
     
    class Meta:
        db_table="coach"

    def __str__(self):
        return f"{self.coach_no} - {self.coach_type.class_name} "

# create model for seat
class seat(models.Model):
    seat_no=models.CharField(max_length=10)
    coach=models.ForeignKey('coach',on_delete=models.CASCADE,to_field='coach_no')
    is_reserved=models.BooleanField(default=False)

    class Meta:
        db_table = "seat"
    def __str__(self):
        return f"{self.seat_no} - {self.coach.coach_no} - {self.coach.coach_type.class_name}"
    
# create models for booking

class ticket_master(models.Model):
    PNR_NO=models.CharField(primary_key=True,max_length=10)
    train_no=models.ForeignKey("train_master", on_delete=models.CASCADE, related_name='tickets')
    arrival_datetime=models.CharField(max_length=255,default=None)
    departure_datetime=models.CharField(max_length=255,default=None)
    depart_station=models.ForeignKey("station_master", on_delete=models.CASCADE,related_name='depart_ticket',to_field="station_code")
    arrival_station=models.ForeignKey("station_master", on_delete=models.CASCADE, related_name='arrival_ticket',to_field="station_code")
    class_id = models.ForeignKey("class_master",on_delete=models.CASCADE,related_name= 'ticket_classes') 
    coach_no=models.ForeignKey("coach",on_delete=models.CASCADE,to_field="coach_no",default=None)
    seat_number = models.CharField(max_length=255)   ## Can be a single number or range of numbers like 1-10  etc.
    fare = models.DecimalField(decimal_places=2, max_digits=8)
    booking_status = [
                 ('R','Reserved'),
                 ('A','Allocated'),
                 ('P','Paid'),
                 ('N','Not Paid'),
                ]
    
    booking_state = models.CharField(max_length=1,choices=booking_status)
    reservation_time = models.DateTimeField(auto_now_add=True)  
    
    class Meta:
            ordering = ['PNR_NO']
    def __str__(self):
        return f"{self.PNR_NO} - {self.train_no} - {self.depart_station} - {self.arrival_station}"

class payment_master(models.Model):
    pnr_no=models.ForeignKey("ticket_master",on_delete=models.CASCADE,related_name='payment')
    card_holdername=models.CharField(max_length=50)
    card_number=models.CharField(max_length=16)
    card_expiry=models.DateField()
    amount_paid=models.DecimalField(decimal_places=2,max_digits=8)
    payment_date=models.DateTimeField(auto_now_add=True)    # auto_now_add=True :- it will automatically add the current date and time when the record is created.  
    payment_choice=[
        ('CNF','CONFIRMED'),
        ('PEN','PENDING'),
    ]
    payment_status=models.CharField(max_length=3,choices=payment_choice)
    payment_method=models.CharField(max_length=10)

