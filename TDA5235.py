from saleae.analyzers import HighLevelAnalyzer, AnalyzerFrame
from enum import Enum
'''
SPI TDA5235 Transaction decoder.
based on SpiTransactionFramer source
'''

class Instruction(Enum):
    Write = 0b00000010 # Write to chip
    Read = 0b00000011 # Read from chip
    ReadFifo = 0b00000100 # Read FIFO from chip
    WriteBurst = 0b00000001 # Write to chip in Burst mode
    ReadBurst = 0b00000101 # Read from chip in Burst mode
    
class Registers(Enum):
    A_MID0 = 0x00 # Message ID Register 0
    A_MID1 = 0x01 # Message ID Register 1
    A_MID2 = 0x02 # Message ID Register 2
    A_MID3 = 0x03 # Message ID Register 3
    A_MID4 = 0x04 # Message ID Register 4
    A_MID5 = 0x05 # Message ID Register 5
    A_MID6 = 0x06 # Message ID Register 6
    A_MID7 = 0x07 # Message ID Register 7
    A_MID8 = 0x08 # Message ID Register 8
    A_MID9 = 0x09 # Message ID Register 9
    A_MID10 = 0x0A # Message ID Register 10
    A_MID11 = 0x0B # Message ID Register 11
    A_MID12 = 0x0C # Message ID Register 12
    A_MID13 = 0x0D # Message ID Register 13
    A_MID14 = 0x0E # Message ID Register 14
    A_MID15 = 0x0F # Message ID Register 15
    A_MID16 = 0x10 # Message ID Register 16
    A_MID17 = 0x11 # Message ID Register 17
    A_MID18 = 0x12 # Message ID Register 18
    A_MID19 = 0x13 # Message ID Register 19
    A_MIDC0 = 0x14 # Message ID Control Register 0
    A_MIDC1 = 0x15 # Message ID Control Register 1
    A_IF1 = 0x16 # IF1 Register
    A_WUC = 0x17 # Wake-Up Control Register
    A_WUPAT0 = 0x18 # Wake-Up Pattern Register 0
    A_WUPAT1 = 0x19 # Wake-Up Pattern Register 1
    A_WUBCNT = 0x1A # Wake-Up Bit or Chip Count Register
    A_WURSSITH1 = 0x1B # RSSI Wake-Up Threshold for Channel 1 Register
    A_WURSSIBL1 = 0x1C # RSSI Wake-Up Blocking Level Low Channel 1 Register
    A_WURSSIBH1 = 0x1D # RSSI Wake-Up Blocking Level High Channel 1 Register
    A_SIGDETSAT = 0x24 # Signal Detector Saturation Threshold Register
    A_WULOT = 0x25 # Wake-up on Level Observation Time Register
    A_SYSRCTO = 0x26 # Synchronization Search Time-Out Register
    A_TOTIM_SYNC = 0x27 # SYNC Timeout Timer Register
    A_TOTIM_TSI = 0x28 # TSI Timeout Timer Register
    A_TOTIM_EOM = 0x29 # EOM Timeout Timer Register
    A_AFCLIMIT = 0x2A # AFC Limit Configuration Register
    A_AFCAGCD = 0x2B # AFC/AGC Freeze Delay Register
    A_AFCSFCFG = 0x2C # AFC Start/Freeze Configuration Register
    A_AFCK1CFG0 = 0x2D # AFC Integrator 1 Gain Register 0
    A_AFCK1CFG1 = 0x2E # AFC Integrator 1 Gain Register 1
    A_AFCK2CFG0 = 0x2F # AFC Integrator 2 Gain Register 0
    A_AFCK2CFG1 = 0x30 # AFC Integrator 2 Gain Register 1
    A_PMFUDSF = 0x31 # Peak Memory Filter Up-Down Factor Register
    A_AGCSFCFG = 0x32 # AGC Start/Freeze Configuration Register
    A_AGCCFG0 = 0x33 # AGC Configuration Register 0
    A_AGCCFG1 = 0x34 # AGC Configuration Register 1
    A_AGCTHR = 0x35 # AGC Threshold Register
    A_DIGRXC = 0x36 # Digital Receiver Configuration Register
    A_PKBITPOS = 0x37 # RSSI Peak Detector Bit Position Register
    A_ISUPFCSEL = 0x38 # Image Supression Fc Selection Register
    A_PDECF = 0x39 # Pre Decimation Factor Register
    A_PDECSCFSK = 0x3A # Pre Decimation Scaling Register FSK Mode
    A_PDECSCASK = 0x3B # Pre Decimation Scaling Register ASK Mode
    A_MFC = 0x3C # Matched Filter Control Register
    A_SRC = 0x3D # Sampe Rate Converter NCO Tune
    A_EXTSLC = 0x3E # Externel Data Slicer Configuration
    A_SIGDET0 = 0x3F # Signal Detector Threshold Level Register - Run Mode
    A_SIGDET1 = 0x40 # Signal Detector Threshold Level Register - Wakeup
    A_SIGDETLO = 0x41 # Signal Detector Threshold Low Level Register
    A_SIGDETSEL = 0x42 # Signal Detector Range Selection Register
    A_SIGDETCFG = 0x43 # Signal Detector Configuration Register
    A_NDTHRES = 0x44 # FSK Noise Detector Threshold Register
    A_NDCONFIG = 0x45 # FSK Noise Detector Configuration Register
    A_CDRP = 0x46 # Clock and Data Recovery P Configuration Register
    A_CDRI = 0x47 # Clock and Data Recovery Configuration Register
    A_CDRRI = 0x48 # Clock and Data Recovery RUNIN Configuration Register
    A_CDRTOLC = 0x49 # CDR DC Chip Tolerance Register
    A_CDRTOLB = 0x4A # CDR DC Bit Tolerance Register
    A_TVWIN = 0x4B # Timing Violation Window Register
    A_SLCCFG = 0x4C # Slicer Configuration Register
    A_TSIMODE = 0x4D # TSI Detection Mode Register
    A_TSILENA = 0x4E # TSI Length Register A
    A_TSILENB = 0x4F # TSI Length Register B
    A_TSIGAP = 0x50 # TSI Gap Length Register
    A_TSIPTA0 = 0x51 # TSI Pattern Data Reference A Register 0
    A_TSIPTA1 = 0x52 # TSI Pattern Data Reference A Register 1
    A_TSIPTB0 = 0x53 # TSI Pattern Data Reference B Register 0
    A_TSIPTB1 = 0x54 # TSI Pattern Data Reference B Register 1
    A_EOMC = 0x55 # End Of Message Control Register
    A_EOMDLEN = 0x56 # EOM Data Length Limit Register
    A_EOMDLENP = 0x57 # EOM Data Length Limit Parallel Mode Register
    A_CHCFG = 0x58 # Channel Configuration Register
    A_PLLINTC1 = 0x59 # PLL MMD Integer Value Register Channel 1
    A_PLLFRAC0C1 = 0x5A # PLL Fractional Division Ratio Register 0 Channel 1
    A_PLLFRAC1C1 = 0x5B # PLL Fractional Division Ratio Register 1 Channel 1
    A_PLLFRAC2C1 = 0x5C # PLL Fractional Division Ratio Register 2 Channel 1
    SFRPAGE = 0x80 # Special Function Register Page Register
    PPCFG0 = 0x81 # PP0 and PP1 Configuration Register
    PPCFG1 = 0x82 # PP2 and PP3 Configuration Register
    PPCFG2 = 0x83 # PPx Port Configuration Register
    RXRUNCFG0 = 0x84 # RX RUN Configuration Register 0
    RXRUNCFG1 = 0x85 # RX RUN Configuration Register 1
    CLKOUT0 = 0x86 # Clock Divider Register 0
    CLKOUT1 = 0x87 # Clock Divider Register 1
    CLKOUT2 = 0x88 # Clock Divider Register 2
    RFC = 0x89 # RF Control Register
    BPFCALCFG0 = 0x8A # BPF Calibration Configuration Register 0
    BPFCALCFG1 = 0x8B # BPF Calibration Configuration Register 1
    XTALCAL0 = 0x8C # XTAL Coarse Calibration Register
    XTALCAL1 = 0x8D # XTAL Fine Calibration Register
    RSSIMONC = 0x8E # RSSI Monitor Configuration Register
    ADCINSEL = 0x8F # ADC Input Selection Register
    RSSIOFFS = 0x90 # RSSI Offset Register
    RSSISLOPE = 0x91 # RSSI Slope Register
    CDRDRTHRP = 0x92 # CDR Data Rate Acceptance Positive Threshold Register
    CDRDRTHRN = 0x93 # CDR Data Rate Acceptance Negative Threshold Register
    IM0 = 0x94 # Interrupt Mask Register 0
    SPMAP = 0x96 # Self Polling Mode Active Periods Register
    SPMIP = 0x97 # Self Polling Mode Idle Periods Register
    SPMC = 0x98 # Self Polling Mode Control Register
    SPMRT = 0x99 # Self Polling Mode Reference Timer Register
    SPMOFFT0 = 0x9A # Self Polling Mode Off Time Register 0
    SPMOFFT1 = 0x9B # Self Polling Mode Off Time Register 1
    SPMONTA0 = 0x9C # Self Polling Mode On Time Config A Register 0
    SPMONTA1 = 0x9D # Self Polling Mode On Time Config A Register 1
    SPMONTB0 = 0x9E # Self Polling Mode On Time Config B Register 0
    SPMONTB1 = 0x9F # Self Polling Mode On Time Config B Register 1
    EXTPCMD = 0xA4 # External Processing Command Register
    CMC1 = 0xA5 # Chip Mode Control Register 1
    CMC0 = 0xA6 # Chip Mode Control Register 0
    RSSIPWU = 0xA7 # Wakeup Peak Detector Readout Register
    IS0 = 0xA8 # Interrupt Status Register 0
    RFPLLACC = 0xAA # RF PLL Actual Channel and Configuration Register
    RSSIPRX = 0xAB # RSSI Peak Detector Readout Register
    RSSIPPL = 0xAC # RSSI Payload Peak Detector Readout Register
    PLDLEN = 0xAD # Payload Data Length Register
    ADCRESH = 0xAE # ADC Result High Byte Register
    ADCRESL = 0xAF # ADC Result Low Byte Register
    VACRES = 0xB0 # VCO Autocalibration Result Readout Register
    AFCOFFSET = 0xB1 # AFC Offset Read Register
    AGCGAINR = 0xB2 # AGC Gain Readout Register
    SPIAT = 0xB3 # SPI Address Tracer Register
    SPIDT = 0xB4 # SPI Data Tracer Register
    SPICHKSUM = 0xB5 # SPI Checksum Register
    SN0 = 0xB6 # Serial Number Register 0
    SN1 = 0xB7 # Serial Number Register 1
    SN2 = 0xB8 # Serial Number Register 2
    SN3 = 0xB9 # Serial Number Register 3
    RSSIRX = 0xBA # RSSI Readout Register
    RSSIPMF = 0xBB # RSSI Peak Memory Filter Readout Register
    SPWR = 0xBC # Signal Power Readout Register
    NPWR = 0xBD # Noise Power Readout Register

class TDA5235(HighLevelAnalyzer):
    """
    Merges SPI frames into transactions based on when the Enable line is active.
    """
    result_types = {
        "TDA5235_reg": {
            "format": "Instruction: {{data.instruction}}, Register: {{data.register}}, Data: {{data.data}}",
        },
        "TDA5235_addr": {
            "format": "Instruction: {{data.instruction}}, Address: {{data.address}}, Data: {{data.data}}",
        },
        "TDA5235Error": {
            "format": "ERROR: {{data.error_info}}",
        }
    }
    
    def __init__(self):
        # Holds the individual SPI result frames that make up the transaction
        self.frames = []

        # Whether SPI is currently enabled
        self.spi_enable = False

        # Start time of the transaction - equivalent to the start time of the "Enable" frame
        self.transaction_start_time = None

        # Whether there was an error.
        self.error = False
        
        # Show register name
        self.show_register_name = True

    def handle_enable(self, frame: AnalyzerFrame):
        self.frames = []
        self.spi_enable = True
        self.error = False
        self.transaction_start_time = frame.start_time
        self.show_register_name = True

    def reset(self):
        self.frames = []
        self.spi_enable = False
        self.error = False
        self.transaction_start_time = None
        self.show_register_name = True

    def is_valid_transaction(self) -> bool:
        return self.spi_enable and (not self.error) and (self.transaction_start_time is not None)

    def handle_result(self, frame):
        if self.spi_enable:
            self.frames.append(frame)

    def get_frame_data(self) -> dict:
        data = bytearray()
        instruction = Instruction(int.from_bytes(self.frames[0].data["mosi"], byteorder='big'))
        address = int.from_bytes(self.frames[1].data["mosi"], byteorder='big')
        
        for frame in self.frames[2:]:
            if instruction in {Instruction.Write, Instruction.WriteBurst}:
                data += frame.data["mosi"]
            else:
                data += frame.data["miso"]
        if self.show_register_name and any(member.value == address for member in Registers):
            result = dict(
                {
                "instruction": instruction.name,
                "register": Registers(address).name,
                "data": bytes(data),
                }
            )
        else:
            result = dict(
                {
                "instruction": instruction.name,
                "address": "0x" + format(address, 'X'),
                "data": bytes(data),
                }
            )
        print(result)
        return result

    def handle_disable(self, frame):
        if self.is_valid_transaction():
            frameData = self.get_frame_data()
            if "register" in frameData:
                result = AnalyzerFrame(
                    "TDA5235_reg",
                    self.transaction_start_time,
                    frame.end_time,
                    frameData,
                )
            else:
                result = AnalyzerFrame(
                "TDA5235_addr",
                self.transaction_start_time,
                frame.end_time,
                frameData,
            )
        else:
            result = AnalyzerFrame(
                "TDA5235Error",
                frame.start_time,
                frame.end_time,
                {
                    "error_info": "Invalid SPI transaction (spi_enable={}, error={}, transaction_start_time={})".format(
                        self.spi_enable,
                        self.error,
                        self.transaction_start_time,
                    )
                }
            )

        self.reset()
        return result

    def handle_error(self, frame):
        result = AnalyzerFrame(
            "SpiTransactionError",
            frame.start_time,
            frame.end_time,
            {
                "error_info": "The clock was in the wrong state when the enable signal transitioned to active"
            }
        )
        self.reset()

    def decode(self, frame: AnalyzerFrame):
        if frame.type == "enable":
            return self.handle_enable(frame)
        elif frame.type == "result":
            return self.handle_result(frame)
        elif frame.type == "disable":
            return self.handle_disable(frame)
        elif frame.type == "error":
            return self.handle_error(frame)
        else:
            return AnalyzerFrame(
                "SpiTransactionError",
                frame.start_time,
                frame.end_time,
                {
                    "error_info": "Unexpected frame type from input analyzer: {}".format(frame.type)
                }
            )
