import logging
import numpy as np
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)

class EMCStandard:

    def __init__(self):
        self.pdf_file = None
        self.name = None
        self.f_avg_limit_mask = None
        self.dbuV_avg_limit_mask = None
        self.f_qp_limit_mask = None
        self.dbuV_qp_limit_mask = None
        self.f_pk_limit_mask = None
        self.dbuV_pk_limit_mask = None

    def load_from_excel(self):
        pass

    def plot_emc_mask(self, fig=None, ax1=None):

        if fig is None and ax1 is None:
            fig, ax1 = plt.subplots(1, 1, figsize=(10, 5))
        # make a little extra space between the subplots
        fig.subplots_adjust(hspace=0.5)
        # TODO: legend, minor grid, manage also peak mask
        ax1.semilogx(self.f_avg_limit_mask, self.dbuV_avg_limit_mask, label = 'avg')
        try:
            ax1.semilogx(self.f_qp_limit_mask, self.dbuV_qp_limit_mask, label = 'qp')
            max_plot= 1.1*max(self.dbuV_qp_limit_mask)
        except:
            logger.warning('No QP limit available for this standard')
        try:
            ax1.semilogx(self.f_pk_limit_mask, self.dbuV_pk_limit_mask, label = 'pk')
            max_plot= 1.1*max(self.dbuV_pk_limit_mask)
        except:
            logger.warning('No PK limit available for this standard')

        ax1.set_xlim(left=10e3, right=50e6)
        # set top as the maximum value of the mask +10% of the mask
        ax1.set_ylim(bottom=0, top=max_plot)
        ax1.set_xlabel('frequency')
        ax1.set_ylabel('Mask [dBuV]')
        ax1.set_title("EMC mask " + self.name)
        ax1.legend()
        ax1.grid(True)

        plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
        plt.savefig(self.name + ".png")

        return fig, ax1

    def interp_log(self, new_frequency):
        ''' here define the limit based on standard available at RFI, see
        /02_Dimensioning_of_circuit_variants/06_Required_EMC_filter_attenuation/EMC_Limits/EMC_Requirements.docx'''

        dbuV_avg_limit = np.interp(x=np.log10(new_frequency), xp=np.log10(self.f_avg_limit_mask),
                                   fp=self.dbuV_avg_limit_mask)
        
        try:
            dbuV_qp_limit = np.interp(x=np.log10(new_frequency), xp=np.log10(self.f_qp_limit_mask),
                                  fp=self.dbuV_qp_limit_mask)
        except:
            dbuV_qp_limit = 0.0
            logger.warning('No QP limit available for this standard')

        try:
            dbuV_pk_limit = np.interp(x=np.log10(new_frequency), xp=np.log10(self.f_pk_limit_mask),
                                  fp=self.dbuV_pk_limit_mask)
        except:
            dbuV_pk_limit = 0.0
            logger.warning('No PK limit available for this standard')

        avg_limit = 10 ** ((dbuV_avg_limit - 120) / 20)
        qp_limit = 10 ** ((dbuV_qp_limit - 120) / 20)
        pk_limit = 10 ** ((dbuV_pk_limit - 120) / 20)

        return avg_limit, qp_limit, pk_limit, dbuV_avg_limit, dbuV_qp_limit, dbuV_pk_limit


class ECE_R10_Conducted_AC_lines(EMCStandard):
    """Table 9: Maximum allowed radiofrequency conducted disturbances on AC power lines"""

    def __init__(self):
        super().__init__()
        self.pdf_file = None
        self.name = "ECE_R_10_2012"
        self.f_avg_limit_mask = [0.15e6, 0.5e6, 0.5e6 + 1, 5e6, 5e6 + 1, 30e6]
        self.dbuV_avg_limit_mask = [56, 46, 46, 46, 50, 50]
        self.f_qp_limit_mask = self.f_avg_limit_mask
        self.dbuV_qp_limit_mask = [66, 56, 56, 56, 60, 60]


class ECE_R10_Conducted_DC_lines(EMCStandard):
    """Table 10: Maximum allowed radiofrequency conducted disturbances on DC power lines"""

    def __init__(self):
        super().__init__()
        self.pdf_file = None
        self.name = "ECE_R_10_2012"
        self.f_avg_limit_mask = [0.15e6, 0.5e6, 0.5e6 + 1, 30e6]
        self.dbuV_avg_limit_mask = [66, 66, 60, 60]
        self.f_qp_limit_mask = self.f_avg_limit_mask
        self.dbuV_qp_limit_mask = [79, 79, 66, 66]


class TL81000_2018_03_AN(EMCStandard):
    """Table 10: Maximum allowed radiofrequency conducted disturbances on DC power lines baseline"""

    def __init__(self, emc_class=5):
        super().__init__()
        self.pdf_file = None
        self.name = "ECE_R_10_2012"
        if emc_class == 3 or emc_class == 4 or emc_class == 5:
            # baseline is the same for all classes
            self.f_avg_limit_mask = [0.15e6, 0.52e6, 0.52e6 + 1, 30e6, 30e6 + 1, 108e6]
            self.dbuV_avg_limit_mask = [97, 65, 65, 65, 55, 55]
            self.f_pk_limit_mask = self.f_avg_limit_mask
            self.dbuV_pk_limit_mask = [107, 75, 75, 75, 65, 65]

class CISPR22(EMCStandard):
    """CISPR22: Information technology equipment - Radio disturbance characteristics - Limits and methods of measurement"""
    def __init__(self, emc_class:str):
        super().__init__()
        self.pdf_file = None
        self.name = "CISPR22_2008_Class_" + emc_class.upper()
        if emc_class.lower() == "a":
            self.f_avg_limit_mask = [0.15e6, 0.5e6, 0.5e6 + 1, 30e6]
            self.dbuV_avg_limit_mask = [66, 66, 60, 60]
            self.f_qp_limit_mask = self.f_avg_limit_mask
            self.dbuV_qp_limit_mask = [79, 79, 73, 73]
        elif emc_class.lower() == "b":
            self.f_avg_limit_mask = [0.15e6, 0.5e6, 0.5e6 + 1, 5e6, 5e6+1, 30e6]
            self.dbuV_avg_limit_mask = [56, 46, 46, 46, 50, 50]
            self.f_qp_limit_mask = self.f_avg_limit_mask
            self.dbuV_qp_limit_mask = [66, 56, 56, 56, 60, 60]
        else:
            raise ValueError("emc_class must be 'A' or 'B'")
        
class CISPR32(CISPR22):
    """CISPR32: Information technology equipment - Radio disturbance characteristics - Limits and methods of measurement"""
    def __init__(self, emc_class:str):
        super().__init__(emc_class)
        self.name = "CISPR32_2015_Class_" + emc_class.upper()

class EN55032(CISPR22):
    """EN55032: Information technology equipment - Radio disturbance characteristics - Limits and methods of measurement"""
    def __init__(self, emc_class:str):
        super().__init__(emc_class)
        self.name = "EN55032_2015_Class_" + emc_class.upper()

class EN55022(CISPR22):
    """EN55022: Information technology equipment - Radio disturbance characteristics - Limits and methods of measurement"""
    def __init__(self, emc_class:str):
        super().__init__(emc_class)
        self.name = "EN55022_2015_Class_" + emc_class.upper()

class FCC47_Part15(CISPR22):
    """FCC47: Information technology equipment - Radio disturbance characteristics - Limits and methods of measurement"""
    def __init__(self, emc_class:str):
        super().__init__(emc_class)
        self.name = "FCC47_2015_Class_" + emc_class.upper()

class EMC_Directive_2014_30_EU(CISPR22):
    """EMC Directive 2014/30/EU: Information technology equipment - Radio disturbance characteristics - Limits and methods of measurement"""
    def __init__(self, emc_class:str):
        super().__init__(emc_class)
        self.name = "EMC_Directive_2014_30_EU_Class_" + emc_class.upper()

class CISPR11(EMCStandard):
    """CISPR11: Industrial, scientific and medical (ISM) radio-frequency equipment - Radio disturbance characteristics - Limits and methods of measurement"""
# https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.academyofemc.com%2Femc-standards&psig=AOvVaw1Qd25JrUxp5zrSDgUaoWUQ&ust=1732471349415000&source=images&cd=vfe&opi=89978449&ved=2ahUKEwjf3JjshPOJAxX66AIHHcV6FLIQjRx6BAgAEBk
    def __init__(self, group:int, power_rating:float, emc_class:str):
        super().__init__()
        self.pdf_file = None
        self.name = f"CISPR11_2015_{power_rating/1e3}kVA_Group_{group}_Class_{emc_class.upper()}"
        if power_rating > 75e3:
            if emc_class.lower() == "a":
                self.f_avg_limit_mask = [0.15e6, 0.5e6, 0.5e6+1, 5e6, 5e6+1, 30e6]
                self.dbuV_avg_limit_mask = [120, 120, 115, 115, 105, 105]
                self.f_qp_limit_mask = self.f_avg_limit_mask
                self.dbuV_qp_limit_mask = [130, 130, 125, 125, 115, 115]
            else:
                raise ValueError("emc_class must be 'A' for power rating > 75kVA")
        else:
            raise NotImplementedError("Power rating <= 75kVA not implemented yet")

class IEC61800_3(EMCStandard):
    """IEC61800-3: Adjustable speed electrical power drive systems - EMC requirements"""
    def __init__(self, emc_class:str, interface:str):
        super().__init__()
        self.pdf_file = None
        self.name = "IEC61800_3_2017_Class_" + emc_class.upper()
        if interface.lower() == "ac":
            if emc_class.lower() == "c1":
                self.f_avg_limit_mask = [0.15e6, 0.5e6, 0.5e6 + 1, 30e6]
                self.dbuV_avg_limit_mask = [66, 66, 60, 60]
                self.f_qp_limit_mask = self.f_avg_limit_mask
                self.dbuV_qp_limit_mask = [79, 79, 73, 73]
            elif emc_class.lower() == "c2":
                self.f_avg_limit_mask = [0.15e6, 0.5e6, 0.5e6 + 1, 5e6, 5e6+1, 30e6]
                self.dbuV_avg_limit_mask = [56, 46, 46, 46, 50, 50]
                self.f_qp_limit_mask = self.f_avg_limit_mask
                self.dbuV_qp_limit_mask = [66, 56, 56, 56, 60, 60]
            else:
                raise ValueError("emc_class must be 'C1' or 'C2' for AC interface")
        elif interface.lower() == "dc":
            if emc_class.lower() == "c1":
                self.f_avg_limit_mask = [0.15e6, 0.5e6, 0.5e6 + 1, 30e6]
                self.dbuV_avg_limit_mask = [80, 80, 74, 74]
                self.f_qp_limit_mask = self.f_avg_limit_mask
                self.dbuV_qp_limit_mask = [80, 80, 74, 74]
            else:
                raise ValueError("emc_class must be 'C1' or for DC interface")

if __name__ == "__main__":
    pass