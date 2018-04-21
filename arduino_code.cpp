#include <dht.h>
#include <DallasTemperature.h>
#include <NMEAGPS.h>
#include <NeoSWSerial.h>

// I connect DHT11 sensor on Arduino's digital pin 7:
#define DHT11_PIN 7

// I connect soil temperature sensor on Arduino's digital pin 22:
#define ONE_WIRE_BUS 22

// Iinitialization of GPS:
#define NMEAGPS_TIMESTAMP_FROM_INTERVAL

NMEAGPS gps;
gps_fix fix;

NeoSWSerial gpsPort(10, 63);

NeoGPS::Location_t GPSLocation;

// Setup a oneWire instance:
OneWire oneWire(ONE_WIRE_BUS);

// Pass our oneWire reference to Dallas Temperature: 
DallasTemperature sensors(&oneWire);

dht DHT;

// This string is for the commands I send from the terminal to the Arduino:
String incomingString;

// Initialization of thresholds. These are set through experinments:
int speed_of_measurements = 0;
float soil_temperature_threshlod = 30.0;
float air_temperature_threshold = 30.0;
float humidity_threshold = 8.0;
int flame_threshold = 900;
int MQ2_threshold = 50;

// Numbering of the node ID and its sensors:
int NODE_ID = 1234;
int GPS_ID = 1;
int HUMIDITY_ID = 1;
int FLAME_ID = 1;
int TEMP_AIR_ID = 1;
int GAS_ID = 1;
int TEMP_SOIL_ID = 1;

// Function reading humidity and returns 1, if the threshold has been exceeded, otherwise returns 0:
int humidity_sensor()
{
    float Value;
    Serial1.print("HUMIDITY#");   
    Serial1.print(HUMIDITY_ID);
    Serial1.print(":");
    Value = DHT.humidity;
    Serial1.print(Value);
    Serial1.print(";");
    if(Value>humidity_threshold)
       return 1;                    
    if(Value<humidity_threshold)
       return 0;                   
}

// Function reading air temperature and returns 1, if the threshold has been exceeded, otherwise returns 0:
int air_temperature()
{
    float Value;
    Serial1.print("TEMP-AIR#");    
    Serial1.print(TEMP_AIR_ID);
    Serial1.print(":");
    Value = DHT.temperature;
    Serial1.print(Value);
    Serial1.print(";");
    if(Value>air_temperature_threshold)
       return 1; 
    if(Value<air_temperature_threshold)
       return 0;
}

// Function sensing flame/fire and returns 1, if the threshold has been exceeded, otherwise returns 0. This function works opposite. 
// When there is fire/flame the sensing value minimizes:
int flame_sensor_read()
{
    int Value;
    Value = analogRead (A0) ;
    Serial1.print("FLAME#");
    Serial1.print(FLAME_ID);
    Serial1.print(":");
    Serial1.print(Value);
    Serial1.print(";");
    if(Value<flame_threshold)
       return 1; 
    if(Value>flame_threshold)
       return 0;
}

// Function reading Gas and returns 1, if the threshold has been exceeded, otherwise returns 0:
int MQ2_sensor()
{
    int Value;
    Value = analogRead (A1) ;
    Serial1.print("GAS#");
    Serial1.print(GAS_ID);
    Serial1.print(":");
    Serial1.print(Value);
    Serial1.print(";"); 
    if(Value>MQ2_threshold)
       return 1;
    if(Value<MQ2_threshold)
       return 0;
}

// Function reading soil temperature and returns 1, if the threshold has been exceeded, otherwise returns 0:
int soil_temperature()
{
    float Value;
    Serial1.print("TEMP-SOIL#");
    Serial1.print(TEMP_SOIL_ID);
    Value = sensors.getTempCByIndex(0);
    Serial1.print(":");
    Serial1.print(Value); 
    Serial1.print(";");
    if(Value>soil_temperature_threshlod)
       return 1; 
    if(Value<soil_temperature_threshlod)
       return 0;
}

void setup() 
{
    Serial1.begin(38400);   // Serial 1 is connected to the Xbee
    gpsPort.begin(9600);    // Starts GPS Serial
    sensors.begin();         
    Serial1.println("STARTING...");
}

void loop() 
{
    Serial1.flush();
    sensors.requestTemperatures();
    DHT.read11(DHT11_PIN);
    int FLAG = 0;
    int speed_;
    float lat_;
    float log_; 
    int date_, month_, year_, hours_, min_, sec_;
    int feedback1 = 0, feedback2 = 0, feedback3 = 0, feedback4 = 0, feedback5 = 0;
    incomingString = Serial1.readString();
    if (incomingString == "SPEED")
    {
        do
        {
             Serial1.println("\nSET SPEED IN SEC = ... ");
             while (Serial1.available() == 0)
             /* just wait */ ;
             speed_ = Serial1.parseInt();
        }while((speed_ < 2) || (speed_ > 86400));             // I give the delay time (frequency of measurements) in seconds. It should be between 2 and 86400.
        speed_of_measurements = (int)((speed_ - 2)/2.016);     // input_output time curve correction 
        Serial1.println(speed_);
    }
  
    while(!gps.available(gpsPort))   // GPS has 1 Hz update signal
       ;
    fix = gps.read();                // get the latest and save it for later
    GPSLocation = fix.location;
    lat_ = fix.latitude();
    log_ = fix.longitude();
    date_ = fix.dateTime.date;
    month_ = fix.dateTime.month;
    year_ = fix.dateTime.year;
    hours_ = (fix.dateTime.hours+2)%24;  // correction of the hour (modulo 24) because I need 24->0, 25->1, 26->2. Also the GPS by mistake is 2 hours back.
    min_ = fix.dateTime.minutes;
    sec_ = fix.dateTime.seconds;
    Serial1.print("UNIQUEID:");
    
// date correction format:
       if(date_ == 0)
    Serial1.print("00");
       else if(date_ == 1)
    Serial1.print("01");
       else if(date_ == 2)
    Serial1.print("02");
       else if(date_ == 3)
    Serial1.print("03");
       else if(date_ == 4)
    Serial1.print("04");
       else if(date_ == 5)
    Serial1.print("05");
       else if(date_ == 6)
    Serial1.print("06");
       else if(date_ == 7)
    Serial1.print("07");
       else if(date_ == 8)
    Serial1.print("08");
       else if(date_ == 9)
    Serial1.print("09");        
       else if(date_ >= 10 && date_ <=31)
    Serial1.print(date_);
    
// month correction format:
    if(month_ == 0)
       Serial1.print("00");
    else if(month_ == 1)
       Serial1.print("01");
    else if(month_ == 2)
       Serial1.print("02");
    else if(month_ == 3)
       Serial1.print("03");
    else if(month_ == 4)
       Serial1.print("04");
    else if(month_ == 5)
       Serial1.print("05");
    else if(month_ == 6)
       Serial1.print("06");
    else if(month_ == 7)
       Serial1.print("07");
    else if(month_ == 8)
       Serial1.print("08");
    else if(month_ == 9)
       Serial1.print("09");        
    else if(month_ >= 10 && month_ <=12)
       Serial1.print(month_);
       
// I let year format as it is:
    Serial1.print(year_);
    
// hours correction format:
    if(hours_ == 0)
       Serial1.print("00");
    else if(hours_ == 1)
       Serial1.print("01");
    else if(hours_ == 2)
       Serial1.print("02");
    else if(hours_ == 3)
       Serial1.print("03");
    else if(hours_ == 4)
       Serial1.print("04");
    else if(hours_ == 5)
       Serial1.print("05");
    else if(hours_ == 6)
       Serial1.print("06");
    else if(hours_ == 7)
       Serial1.print("07");
    else if(hours_ == 8)
       Serial1.print("08");
    else if(hours_ == 9)
       Serial1.print("09");        
    else if(hours_ >= 10 && hours_ <=24)
       Serial1.print(hours_);
       
// minutes correction format:          
    if(min_ == 0)
       Serial1.print("00");
    else if(min_ == 1)
       Serial1.print("01");
    else if(min_ == 2)
       Serial1.print("02");
    else if(min_ == 3)
       Serial1.print("03");
    else if(min_ == 4)
       Serial1.print("04");
    else if(min_ == 5)
       Serial1.print("05");
    else if(min_ == 6)
       Serial1.print("06");
    else if(min_ == 7)
       Serial1.print("07");
    else if(min_ == 8)
       Serial1.print("08");
    else if(min_ == 9)
       Serial1.print("09");        
    else if(min_ >= 10 && min_ <=59)
       Serial1.print(min_);
       
// seconds correction format:
    if(sec_ == 0)
       Serial1.print("00");
    else if(sec_ == 1)
       Serial1.print("01");
    else if(sec_ == 2)
       Serial1.print("02");
    else if(sec_ == 3)
       Serial1.print("03");
    else if(sec_ == 4)
       Serial1.print("04");
    else if(sec_ == 5)
       Serial1.print("05");
    else if(sec_ == 6)
       Serial1.print("06");
    else if(sec_ == 7)
       Serial1.print("07");
    else if(sec_ == 8)
       Serial1.print("08");
    else if(sec_ == 9)
       Serial1.print("09");
    else if(sec_ >= 10 && sec_ <=59)
       Serial1.print(sec_); 

// The rest of the data to be sent:
    Serial1.print(";");
    Serial1.print("NODEID:");
    Serial1.print(NODE_ID);
    Serial1.print(";");
    Serial1.print("GPS#");
    Serial1.print(GPS_ID);
    Serial1.print(":");
    Serial1.print(lat_,6);
    Serial1.print( ',' );
    Serial1.print(log_,6);
    Serial1.print(";");
    Serial1.print("EPOCH:");

// This is for epoch format printing:
    if (fix.valid.date && fix.valid.time) 
    {
        NeoGPS::clock_t Y2Kseconds  = fix.dateTime;
        NeoGPS::clock_t UNIXseconds = Y2Kseconds + 946684800UL; // more seconds to older epoch
        Serial1.print(UNIXseconds);
    }

    Serial1.print(";");
    feedback1 = humidity_sensor();
    feedback2 = flame_sensor_read();
    feedback3 = air_temperature();
    feedback4 = MQ2_sensor();
    feedback5 = soil_temperature();
    Serial1.println();
    if((!feedback1) && (!feedback2) && (!feedback3) && (!feedback4) && (!feedback5))  // if no threshold has been exceeded...
    {
        for(int i=0; i<speed_of_measurements; i++)
        {
            delay(1000);  
            
// if a threshold has been exceeded, break for loop and go at the begining of void loop():   
            if(
               ((float)DHT.humidity > humidity_threshold) ||
               ((float)DHT.temperature > air_temperature_threshold) ||
               (analogRead(A0) < flame_threshold) ||
               (analogRead(A1) > MQ2_threshold)  ||
               (sensors.getTempCByIndex(0) > soil_temperature_threshlod))
               {
                     FLAG = 1;            
                     break;
               }
            incomingString = Serial1.readString();

// If inside the delay of measurements a new command is sent from the terminal to the Arduino, Arduino should handle it:
            if (incomingString == "SPEED" && FLAG == 0)
            {
                do
                {
                    Serial1.println("\nSET SPEED IN SEC = ... ");
                    while (Serial1.available() == 0)
                    /* just wait */ ;
                    speed_ = Serial1.parseInt();
                }while((speed_ < 2) || (speed_ > 86400));            // I give the delay time (frequency of measurements) in seconds. It should be between 2 and 86400.
                speed_of_measurements = (int)((speed_ - 2)/2.016);    // input_output time curve correction
                Serial1.println(speed_);
            }
        }   
    }   
}  
