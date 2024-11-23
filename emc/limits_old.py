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

    def plot_emc_mask(self):
        fig, ax1 = plt.subplots()
        # make a little extra space between the subplots
        fig.subplots_adjust(hspace=0.5)
        # TODO: legend, minor grid, manage also peak mask
        ax1.semilogx(self.f_avg_limit_mask, self.dbuV_avg_limit_mask, self.f_qp_limit_mask, self.dbuV_qp_limit_mask)
        ax1.set_ylim(bottom=0)
        ax1.set_xlabel('frequency')
        ax1.set_ylabel('avg, qp')
        ax1.grid(True)
        plt.savefig(self.name + ".png")

        return 0

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



if __name__ == "__main__":
    pass