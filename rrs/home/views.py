from django.db.models import Count
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import  login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render    
from .forms import *
import json
from django.core.serializers.json import  DjangoJSONEncoder
from .models import *
from datetime import datetime
from django.contrib.auth.hashers import make_password ,check_password
from datetime import datetime,date,timedelta




def index(request):
    # return HttpResponse('hello')
    stn =station_master.objects.all()
    clss=class_master.objects.all()
    return render(request, 'index.html', {'title': 'Home', 'stn': stn,'clss':clss})

def register(request):
    if request.method == 'POST':

       username = request.POST.get('username')
       password = request.POST.get('password')
       firstname = request.POST.get('firstname')
       lastname = request.POST.get('lastname')
       dob = request.POST.get('dob')
       email = request.POST.get('email')
       mobile = request.POST.get('mobile')
       address = request.POST.get('address')
       # for save the information of user 

       if user_master.objects.filter(username = username).exists():
            messages.error(request, "Username already exists. Give different name")
            return redirect('/register')
       else:
            myuser = user_master(firstname=firstname, lastname=lastname, username=username,
            password=password, dob=dob, email=email, mobile=mobile, address=address)
            myuser.save()
            return  redirect('/login')
    return render(request, 'register.html')


# fuction to check the login or handle login request
def handlelogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username,password)
        try:
            
            user = user_master.objects.get(username=username, password=password)
            request.session['username'] = user.username
            if user.username == 'admin' :
                return redirect('/adminpanel')
            
            print('User Logged In Successfully!')
            return redirect('/dashboard')
            # else:
            #     return HttpResponse( "Invalid Login")
            

        except user_master.DoesNotExist:
            messages.error(request, "User does not exist")
            return redirect('/login')
                    
    return render(request,'login.html')


def logout_view(request):
        logout(request)
        return redirect('/login')        


#@login_required(login_url='/login')
def dashboard(request):
    stn =station_master.objects.all()
    clss=class_master.objects.all()
    

    print(request.user)
    # Get the logged in users id from session and get all data related to that user
    user_name=request.session.get('username')
    user_name = {
        'User' : user_name
        
    }
    # get the current logged in user details from session and display on dashboard page
    return render(request, 'dashboard.html',{ 'stn': stn,'clss':clss,'user':user_name})

def about(request):
    return HttpResponse('this is for about information of our admin. ')

def contact(request):
    return HttpResponse('this is for contact information of our admin. ')


def schedules(request):
    if request.method=='POST':
        trn_no=request.POST.get('trn_no')
        trn_sch=train_schedule.objects.filter(train_no=trn_no)
        print(trn_sch)
        for i in trn_sch:
            tno=i.train_no
            st=i.station_code

        return HttpResponse(tno,st)
    return render(request,'trnschdle.html')


def pnr_status(request):
    #return HttpResponse('this page is for check pnr status of a particular train.')
    if request.method== "POST":
        pnr = request.POST.get('pnr')
        print(pnr)
        ticket=ticket_master.objects.filter(PNR_NO=pnr)
        print(ticket)
        # for i in ticket:
        #     clas_id=i.class_id
        # print(clas_id,"class_id")
        # clas=class_master.objects.filter(class_id=clas_id)
        # print(clas)
        # for i in clas:
        #     class_name=i.class_name
        # print(class_name)
        paxs=passenger_master.objects.filter(pnr_no_id=pnr)
        print(paxs)
        print("POST condition")
        if ticket:
            return render(request,'pnr.html',{'ticket':ticket,'paxs':paxs})
        else:
           messages.error(request,"Invalid PNR Number")

       
    return render(request,'pnr.html')

def cancel_ticket(request):
    
    if request.method=='POST':
        pnr=request.POST.get('pnr')
        ticket=ticket_master.objects.filter(PNR_NO=pnr)
        if ticket:
            ticket.delete()
            messages.success(request,"Your ticket has been cancelled successfully!")
            print("deleted.")
            return render(request,'cancel.html',{'msg':'Your ticket has been cancelled successfully!'})
        else:
            print("already deleted.")
            messages.error(request,"Invalid PNR Number")
    # return HttpResponse("This Page Is For Canceling Tickets")
    return  render(request,"cancel.html",{'msg':'Please enter your ticket number to proceed.'})


def feedback(request):
     #return HttpResponse('this page for user give the feedback or suggestiions.')
     if request.method =="POST":
          email= request.POST['email']
          subject= request.POST['subject']
          descrip = request.POST['descrip']
          username=request.session.get('username')
        #   username={
        #       'User':username
        #   }
          user= user_feedback(subject=subject, message=descrip,email=email,username=username)
          user.save()

          
     return render(request,'feedback.html')


#from django.core.mail import send_mail
#def thankyou(request):
    #return render(request,'thankyou.html')
# register
        

# add schedule of train
def addschedule(request):
    trn=train_master.objects.all()
    stn=station_master.objects.all()
    
    if request.method=='POST':
        train_no=request.POST.get('train_no')
        station_code=request.POST.get('station_code')
        stop_time=request.POST.get('stop_time')
        depart_time=request.POST.get('depart_time')
        arrival_time=request.POST.get('arrival_time')
        distance=request.POST.get('distance')
        day=request.POST.get('day')
        seq=request.POST.get('seq')
        par_stoptime=datetime.strptime(stop_time, '%H:%M').time()
        print(train_no,station_code,stop_time,depart_time,arrival_time,distance,day,seq)
        train=train_schedule(train_no_id=train_no, station_code_id=station_code, stop_time=par_stoptime, depart_time=depart_time, arrival_time=arrival_time, distance=distance, day=day, seq=seq)
        print(train)
    return render (request,'addsch.html',{'trn':trn,'stn':stn})


# addd trains in database

def addtrains(request): 
     source_stations=station_master.objects.all()
     dest_stations=station_master.objects.all()
     context= {'source_stations':source_stations , 'dest_stations':dest_stations}
     if  request.method == 'POST' :
               train_no= request.POST.get('train_no')
               train_name = request.POST.get('train_name')
               src = request.POST.get('source_station')
               dest = request.POST.get('dest_station')
               depart_time = datetime.strptime(request.POST.get('depart_time'), '%H:%M').time()
               arrival_time = datetime.strptime(request.POST.get('arrival_time'), '%H:%M').time()
               journey_duration= request.POST.get('journey_duration')
               
               try:
                   source_station=station_master.objects.get(station_code=src)
                   dest_station=station_master.objects.get(station_code=dest)

               except station_master.DoesNotExist:
                   return HttpResponse("Station does not exist")
                   
               new_train = train_master(train_no=train_no,train_name=train_name, source_station=source_station, dest_station=dest_station,depart_time=depart_time,
                                        arrival_time=arrival_time,journey_duration=journey_duration)
               new_train.save()
               return render(request,'addtrains.html')
            
            
     else:
          HttpResponse("Something wrong. Please try again.")
            
     return render(request,'addtrains.html',context)

def addstation(request):
    if request.method == 'POST':
            station_name = request.POST['station_name'].upper()
            station_code= request.POST['station_code'].upper()
            location= request.POST['location']
            zone= request.POST['zone'].upper()  
            state= request.POST['state'].upper()
            new_station=station_master(station_name=station_name,station_code=station_code,location=location,zone=zone,state=state)
            new_station.save()
            return render(request,'station.html.')  # Replace 'success_page' with the URL to redirect after successful form submission
    else:
        HttpResponse("something wrong. please try again")

    return render(request, 'station.html')
def addroutestn(request):
    stn=station_master.objects.all()
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        query = request.GET.get('term', '')
        stations = station_master.objects.filter(station_name__icontains=query)
        results = [station.station_name for station in stations]
        return JsonResponse(results, safe=False)
    return render(request, 'routestation.html')

    # if request.method == 'POST':
    #     train_no=request.POST['train_no']
    #     station_id = request.POST['station_id']
    #     sequence_no = request.POST['sequence_no']
    #     arrival_time=datetime.strptime(request.POST['arrival_time'], "%H:%M").time()
    #     departure_time=datetime.strftime(request.POST['departure_time'],"%H:%M").time()
    #     print (type(arrival_time))
    #     route=routestation(train_no=train_no,station_id=station_id,sequence_no=sequence_no,arrival_time=arrival_time,departure_time=departure_time)
    #     route.save()
        
    #     return HttpResponse ("Route added successfully")
    # else:
    #       HttpResponse("Error in adding Route") 
    # return render(request,"routestation.html")


def searchtrain(request):
    # get the data from the user
    if request.method == 'POST':
        source = request.POST.get("source") 
        destination = request.POST.get("destination")
        depart_date= request.POST.get("depart_date")
        clss=int(request.POST.get( "class"))
        
        
        # dep_date=datetime.strptime(depart_date, "%Y-%m-%d").date()
        # print(dep_date)
        # Query trains based on source station and destination station
        print(source,destination,type(depart_date))
        stn_src = station_master.objects.filter(station_code = source)
        print(stn_src)
        for station in stn_src:
            source_names = station.station_name
            
        print(source_names) 
        stn_des = station_master.objects.filter(station_code = destination)
        print(stn_des)
        for station in stn_des:
            des_names = station.station_name
        print(des_names)
        
        filtered_trains=[]
        # get the train number from the train_schedule table
        # rdes is destination search from train_schedule table
        rdes = train_schedule.objects.filter(
        
            station_code_id=destination,
        ).values()
        
        print(rdes)
        for  i in rdes:
             t_no=i["train_no_id"]
             print("the t_no  ",t_no)
             # distance of destination
             ddist = i['distance']
             print(ddist)
             day=i['day']
             arr=str(i['arrival_time'])
             print("this is for arival time",arr)
             # sdes is source search from train_schedule table and check train_no_id of source matches with rdes
             sdes=train_schedule.objects.filter(train_no_id = t_no,station_code_id=source).values()
             print("sdes",sdes)
             # if  condition aayegi sdes agr khali hai toh
             if len(sdes)==0:
                 print("sdes is empty")
                 break
             else:      
                for  j in sdes:
                     print(j['station_code_id'])
                     # distance at source
                     sdist=j['distance']
                     print(sdist,"is the dist from source")
                     depart_time=str(j['depart_time'])
                     # check that depart time is after the current time or not  
                     depat_time=datetime.strptime(depart_date+' '+depart_time, '%Y-%m-%d %H:%M:%S')
                     print(depat_time)
                     current_time=datetime.now()
                     print(current_time)
                     if depat_time < current_time:
                 
                        print("depart time is less than current time")
                        break
                        # if depart time is less than current time then check for next day
                    
                     else:

                        print("depart time.",depart_time)
                        print(j['seq'],i['seq'])

                        if j['seq'] < i['seq'] :
                      
                            t_name = train_master.objects.filter(train_no=t_no).values()
                            for  k in t_name:
                         
                                filtered_trains.append(k)

                # find tottal diatance between source and detination
                total_dist=int(ddist)-int(sdist)
                print(total_dist,"is the total distance.",clss)
                if(clss==1):
                    fare=total_dist*0.80
                elif(clss==2):
                    fare=(total_dist*0.80)*2
                elif(clss==3):
                    fare=(total_dist*0.80)*3
                else:
                    fare=(total_dist*0.80)*4
              
                # parsed date of depart,time and arrival time
                dep_datetime=datetime.strptime(depart_date+' '+depart_time,'%Y-%m-%d %H:%M:%S')
                arr_time=datetime.strptime(arr, '%H:%M:%S').time()

                # calculate arivaldatetime
                if arr_time < dep_datetime.time() :
                    arr_datetime=dep_datetime + timedelta(days=1)
                else:
                    arr_datetime=dep_datetime
            
                arr_date = arr_datetime.strftime('%Y-%m-%d')
                print("filters trains",filtered_trains)
        station = {
            'src': source_names,
            'dest':des_names,
            
        }
        print(station)   
        if len(filtered_trains)==0 :  # Check if filtered_trains is empty
            messages.error(request, "No trains found")
            filtered_trains_serialized=[]
            print("if condition")
        else:    
           
            # Convert time objects to strings
            filtered_trains_serialized = []
            for train in filtered_trains:
                train_data = {
                    'train_no': train['train_no'],
                    'train_name': train['train_name'],
                    # Convert time objects to strings
                    'arrival_time': str(train['arrival_time']),
                    'departure_time': str(train['depart_time']),
                    'journey_duration': train['journey_duration'],
                    # Add other fields as needed
                }

            filtered_trains_serialized.append(train_data)
        
           
            #print(t_no,sdes)
       

            print(type(arr),type(arr_date))
            dat={
                'arrival_time':arr,
                'depart_time':str(depart_time),
                'depart_date':str(depart_date),
                'arrival_date':arr_date
            }
            request.session["dat"]= json.dumps(dat,cls=DjangoJSONEncoder) 
            request.session["fare"]=fare
            request.session["clss"]=clss
         # Store the serialized data in the session
        request.session["info"] = json.dumps({"trains": filtered_trains_serialized, "station": station}, cls=DjangoJSONEncoder)      
       
       
        return HttpResponseRedirect('/displaytn')
        # return render(request,"searchedtrains.html",{ "trains": filtered_trains , "station": station})
       #You can do further processing with the 'trains' queryset

    else:
        # If it's a GET request, create an empty form
      print("else condn chal rhi hai")

    return render(request, 'srchtrn.html' )
def displaytn(request):          
     session_data_json=request.session.get('info')
     print ("Session Data Json ",type(session_data_json))
     fare=request.session.get('fare',None)
     datee=request.session.get( 'dat', None)
     dat=json.loads(datee) 
     if  not session_data_json :
          return HttpResponseRedirect('/dashboard')
     else:  
          session_data=json.loads(session_data_json)
          stations=session_data.get('station',{})
          trains=session_data.get('trains',[])
          print(stations)
         
     return  render(request,'searchedtrains.html',{"trains":trains,'station':stations,'fare':fare,'dat':dat}) 
    
     
def addpass(request):      
     return render(request, 'addpass.html')

#here we have all details of passengers and their respective trains. which will be  sent to payment gateway for booking ticket.
def reviewdetails(request):
    if  request.method=='POST':

        passenger_count = int(request.POST.get('passengerCount', 0))
        print(passenger_count)
       
        passengers = []
        for i in range(1, passenger_count + 1):
                
            name = request.POST.get(f'name{i}', '')
            age = int(request.POST.get(f'age{i}', 0))
            gender = request.POST.get(f'gender{i}','')
            passengers.append({'name': name, 'age': age, 'gender': gender })
            # passen=passenger_master(name=name,age=age,gender=gender)
            # passen.save()
        
        request.session['passengers'] = passengers
        print("passengers information in add passengers.",passengers)
    session_data_json= request.session.get('info')
    session_data=json.loads(session_data_json)
    station=session_data.get("station",{})
    print(station)
    trains=session_data.get("trains",[])
    dat=request.session.get('dat')
    dat=json.loads(dat)
    classes=request.session.get('clss')
    cls=class_master.objects.get(class_id=classes)
    clss=cls.class_name
    print(trains)
    passengers=request.session.get('passengers',None)
    tot_fare=request.session.get('fare')
    if passengers is not None:
        tot_pass=len(passengers)
        tot_fare=tot_fare*tot_pass
        request.session['tot_fare']=tot_fare
        print(passengers)
        return render(request,'revtktdet.html',{"trains":trains,"station":station,"paxs":passengers,'fare':tot_fare,'dat':dat,'clss':clss})
       
    else:
        return HttpResponseRedirect('/addpassengers')

    
    #    return render(request,'bookingdetail.html',context)    

# @login_required
# def booknow(request):
#    try:
#       user=User.objects.get(username=request.user.username)
#       info=request.session.get('info')
#       if not info:
#           return HttpResponseRedirect('/searchTrain')
#       else:
#            stns=info["stations"]
#            trns=info["trains"]
#            paxs=request.session.get('passengers')
#            bkng=ticket_master(user=user,train=trns[0],from_station=stns[0].id,to_station=stns[1].id,no_of_passengers=len
def payment(request):
    tot_fare=request.session.get('tot_fare')
    if request.method=="POST":
            name=request.POST.get('cardholder')
            card_no=request.POST.get('cardnumber')
            # card_type=request.POST.get('card_type')
            expiry_date=request.POST.get('expiry')
            card_cvv=request.POST.get('cvv')
            print(name,card_no,expiry_date,card_cvv)
            pay_det={
                'name':name,
                'card_no':card_no,
                'expiry_date':expiry_date,
                'card_cvv':card_cvv,
            }
            # if len(pay_det)!=0:
            #     request.session['pay_det']=pay_det
            #     return HttpResponseRedirect('/booking')
            # else:
            #     return HttpResponse("payment failed")
            
            
    return render(request,"payment.html",{'fare':tot_fare})

import random
import string
def booking(request):
     """Generate a random PNR number."""
     pnr=''.join(random.choices( string.digits, k=10))
     session_data_json=request.session.get('info')  # train data session 
     session_data=json.loads(session_data_json)  # load the train data session
     stations=session_data.get("station",{}) #station data session
     trains=session_data.get("trains",[]) #train data session
     class_id=request.session.get('clss')      # having clas_id in the session
     passengers=request.session.get('passengers') 
     tot_fare=request.session.get('tot_fare')
     datt=request.session.get('dat')  # session of arrival date , depart_date , arrival_time and depart_time.
     dat=json.loads(datt)
     num_passengers=len(passengers)

     if stations:
         src=station_master.objects.filter(station_name=stations['src'])
         for i in src:
             srcstation_code=i.station_code
         srcinst=station_master.objects.get(station_code=srcstation_code)
         dest=station_master.objects.filter(station_name=stations['dest'])
         for i in dest:
             desstation_code=i.station_code
         destinst=station_master.objects.get(station_code=desstation_code)

     classinst=class_master.objects.get(class_id=class_id)
     clas=classinst.class_name
# Find available coaches for the given train, class, and station
     available_coaches = coach.objects.filter(
        coach_type=class_id,
        seat__is_reserved=False
     ).distinct()
     print("availavle coach",available_coaches)
     if not available_coaches:
        raise Exception("No available coaches found.")
        # Get the first available coach
     coache = available_coaches.first()
     print("coache",coache)
     
        # Get the number of available seats in the coach
     available_seat_count =seat.objects.filter(coach_id=coache.coach_no,is_reserved=False).count()
     print("availabke seat_count",available_seat_count)
     if available_seat_count < num_passengers:
        raise Exception("Insufficient available seats.")

        # Reserve seats in the coach
     reserved_seats = []
     for _ in range(num_passengers):
        available_seat = seat.objects.filter(coach_id=coache.coach_no,is_reserved=False).first()
        available_seat.is_reserved = True
        available_seat.save()
        reserved_seats.append(available_seat.seat_no)
     print("reserved seats",reserved_seats)
     # combine datetime field
     
     arival_da=f"{ dat['arrival_date'] } { dat['arrival_time'] }"
     depart_da=f"{ dat['depart_date'] } { dat['depart_time'] }"
     print(arival_da,depart_da)
        # Create a ticket for the booking
     ticket = ticket_master.objects.create(
        PNR_NO=pnr,
        train_no_id=trains[0] ['train_no'],
        departure_datetime=depart_da,
        arrival_datetime=arival_da,
        depart_station=srcinst,
        arrival_station=destinst,
        class_id=classinst,
        coach_no=coache,
        seat_number=", ".join(reserved_seats),
        fare=tot_fare,  #  calculated fare in search train function.
        booking_state='R'  # Assuming booking status is 'Reserved'
        )
     print("successfully booked.")
        # Create passenger entries associated with the ticket
     # Iterate through each passenger and assign a seat number
     for index, passenger_data in enumerate(passengers):
        seat_number = reserved_seats[index]  # Get the corresponding reserved seat number
        passenger_master.objects.create(
            name=passenger_data['name'],
            age=passenger_data['age'],
            gender=passenger_data['gender'],
            pnr_no=ticket,
            seat_no=seat_number  # Assign the seat number to the passenger
        )
     print("passengers added sucessfully.")

     # passenger data display in the final ticket page(booking.html)
     passdata=[]
     pas=passenger_master.objects.filter(pnr_no_id=pnr)
     print(pas)
     for i in pas:
         pas_name=i.name
         pas_age=i.age
         pas_gender=i.gender
         pas_seat=i.seat_no
     passdata.append({'pas_name':pas_name,'pas_age':pas_age,'pas_gender':pas_gender,'pas_seat':pas_seat})
     print(passdata)
         
     request.session.flush()

     print(pnr)
    #  return HttpResponse("booking done.")
     return render(request,"booking.html",{'pnr':pnr,'trains':trains,'station':stations,'paxs':passdata,'fare':tot_fare,'dat':dat,'clas':clas,'coache':coache})

# for clear all seat
# seat.objects.all().update(is_reserved=False)
# create admin panel  function 
def admin_panel(request):
    return render(request,"admin.html")

def manage_feedback(request):
    feedbacks = user_feedback.objects.all()
    return render(request,"mngfeed.html",{'feedbacks':feedbacks})

def manage_trains(request):
    trains = train_master.objects.all()
    return render(request,"mange_trains.html",{'trains':trains})





