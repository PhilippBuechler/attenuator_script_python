requirement to use this script:

Python version 3.7
pySerial module

usage:
        -h --help                               shows the help

        -p --port       [serialport]            path to serial port the device is in
                                                this option is required for every function except help

        -s --set_value  [chain:attenuation]    sets given chain to a given attenuation.
                                                available chains: 1 2 3 4
                                                attenuation needs to be between 0 and 95dB
                                                the resolution is 0.25dB

        -t --csv_table  [path to csv file]      instructs the attenuator to run an attenuation pattern
                                                when using this option the script needs to be terminated manually
                                                see in readme how the csv file needs to be filled

        -i --info                               reads out the status of the device

        --portinfo                              shows list of connected serial devices



the csv file should be structed as followed:

duaration_time_in_milliseconds;attenuation_chain1;attenuation_chain2;attenuation_chain3;attenuation_chain4

the script will set the chains and then wait the duaration time until going to the next line
