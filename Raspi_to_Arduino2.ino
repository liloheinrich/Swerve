// Example 5 - Receive with start- and end-markers combined with parsing

const byte numChars = 64;
char receivedChars[numChars];
char tempChars[numChars];        // temporary array for use when parsing

// variables to hold the parsed data
float motor4_speed = 0.0;
int servo1_angle = 0;
int servo2_angle = 0;
int servo3_angle = 0;
int servo4_angle = 0;

boolean newData = false;

//============

void setup() {
    Serial.begin(9600);
//    Serial.println("This demo expects 5 pieces of data - float motor4_speed, and 4 integer servo angles");
//    Serial.println("Enter data in this style <0.676, 12, 24, 171, 90>  ");
//    Serial.println();
}

//============

void loop() {
    recvWithStartEndMarkers();
    if (newData == true) {
        strcpy(tempChars, receivedChars);
            // this temporary copy is necessary to protect the original data
            //   because strtok() used in parseData() replaces the commas with \0
        parseData();
        showParsedData();
        newData = false;
    }
}

//============

void recvWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char rc;

    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        if (recvInProgress == true) {
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }

        else if (rc == startMarker) {
            recvInProgress = true;
        }
    }
}

//============

void parseData() {      // split the data into its parts

    char * strtokIndx; // this is used by strtok() as an index

    strtokIndx = strtok(tempChars, ",");
    motor4_speed = atof(strtokIndx);     // convert this part to a float

    strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
    servo1_angle = atoi(strtokIndx);     // convert this part to an integer

    strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
    servo3_angle = atoi(strtokIndx);     // convert this part to an integer

    strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
    servo3_angle = atoi(strtokIndx);     // convert this part to an integer

    strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
    servo4_angle = atoi(strtokIndx);     // convert this part to an integer
}

//============

void showParsedData() {
    Serial.print(motor4_speed);
    Serial.print(", ");
    Serial.print(servo1_angle);
    Serial.print(", ");
    Serial.print(servo2_angle);
    Serial.print(", ");
    Serial.print(servo3_angle);
    Serial.print(", ");
    Serial.println(servo4_angle);
}
