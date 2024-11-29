# /usr/bin/env python3
# -*- coding: utf-8 -*-
# Created on 

import logging
import numpy as np
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)


class WeightedEfficiency:
    def __init__(self, power_levels, weights=None, name="Generic Weighted Efficiency"):

        self.name = name
        self.power_levels = power_levels
        # self.efficiencies = efficiencies
        if weights is None:
            # Default weights (equal weights)
            self.weights = [1 / len(power_levels)] * len(power_levels)
        else:
            self.weights = weights

    def calculate_weighted_efficiency(self, power_levels_inputs, efficiencies_inputs):
        """
        Calculate the weighted efficiency based on the given power levels, efficiencies, and weights.
        
        Returns:
        float: Weighted efficiency as a decimal (e.g., 0.945 for 94.5%).
        """
        if len(power_levels_inputs) != len(efficiencies_inputs) or len(power_levels_inputs) != len(self.weights):
            raise ValueError("Lengths of power levels, efficiencies, and weights must be the same.")

        self.power_levels = np.array(power_levels_inputs)
        self.efficiencies = np.array(efficiencies_inputs)
        
        weighted_efficiency = np.sum(self.weights * self.efficiencies)

        self.weighted_efficiency = weighted_efficiency
        return weighted_efficiency

    def plot_efficiency(self):
        """
        Plot the efficiency curve with power levels and efficiency values.
        """
        weighted_eff = self.weighted_efficiency # Convert to percentage
        
        fig, ax1 = plt.subplots(figsize=(10, 8))

        # Plot efficiency as a line
        ax1.plot(self.power_levels, self.efficiencies,
                 marker='o', color='b', label="Efficiency at Power Levels")
        ax1.set_xlabel("% of Rated Output Power", fontsize=12)
        ax1.set_ylabel("Efficiency (%)", fontsize=12, color='b')
        # ax1.set_ylim(80, 100)  # Assuming efficiencies are typically within 80-100%
        ax1.tick_params(axis='y', labelcolor='b')
        ax1.set_title(f"CEC Weighted Efficiency = {weighted_eff:.2f}%", fontsize=14)
        ax1.legend(loc='upper left', fontsize=10)
        ax1.grid(True)

        # Add bar chart for weights
        ax2 = ax1.twinx()  # Create a second y-axis
        ax2.bar(self.power_levels, self.weights, width=5, color='orange', alpha=0.6, label="Weighting Factors")
        ax2.set_ylabel("Weighting Factor", fontsize=12, color='orange')
        ax2.tick_params(axis='y', labelcolor='orange')
        ax2.set_ylim(0, max(self.weights) * 1.5)
        ax2.legend(loc='upper right', fontsize=10)

        # Add logo to the plot in background middle
        logo = plt.imread('./logo.png')
        fig.figimage(logo, 100, 100, alpha=0.2)

        plt.tight_layout()
        plt.show()

class SolarCECweightedEfficiency(WeightedEfficiency):
    def __init__(self):
        super().__init__(
            name="Solar CEC Weighted Efficiency",
            power_levels = [5, 10, 20, 30, 50, 75, 100],  # % of rated output power
            weights = [0, 0.04, 0.05, 0.12, 0.21, 0.53, 0.05],  # Weighting factors
        )

class SolarEUweightedEfficiency(WeightedEfficiency):
    def __init__(self):
        super().__init__(
            name="Solar EU Weighted Efficiency",
            power_levels = [5, 10, 20, 30, 50, 75, 100],  # % of rated output power
            weights = [0.03, 0.06, 0.13, 0.10, 0.48, 0, 0.20],  # Weighting factors
        )




class EfficiencyLimits:
    def __init__(self):
        self.name = None
        self.load_levels = None  # Load levels in percentages (e.g., 20, 50, 100)
        self.efficiency_levels = None  # Efficiency levels as floats (e.g., 0.8 for 80%)

    def plot_efficiency(self, fig=None, ax1=None):
        if fig is None and ax1 is None:
            # fig, ax1 = plt.subplots(1, 1, figsize=(10, 5))
            pass
        
        # Convert efficiency levels to percentages for plotting
        efficiency_percentages = [eff * 100 for eff in self.efficiency_levels]
        
        # Plot efficiency data
        ax1.plot(self.load_levels, efficiency_percentages, marker='o', label=self.name)
        # plot red fill below the curve
        ax1.fill_between(self.load_levels, efficiency_percentages, 50, color='red', alpha=0.1)
        
        # add logo to the plot in the bottom right corner background
        logo = plt.imread('./logo.png')
        ax1.imshow(logo, alpha=0.2, extent=(60, 100, 50, 80))

    
        # Configure plot
        ax1.set_xlim(0, 100)
        ax1.set_ylim(50, 100)
        ax1.set_xlabel('Load Level (%)')
        ax1.set_ylabel('Efficiency (%)')
        ax1.set_title(f"Efficiency Profile - {self.name}")
        ax1.grid(True)
        ax1.legend()

        # plt.savefig(self.name + ".png")
        # plt.show()

        return fig, ax1

class EfficiencyCertification(EfficiencyLimits):
    """Class for plotting efficiency certifications like 80 PLUS Standard."""

    def __init__(self, certification_name, load_levels, efficiency_levels):
        super().__init__()
        self.name = certification_name
        self.load_levels = load_levels
        self.efficiency_levels = efficiency_levels

class EightyPlusStandard(EfficiencyCertification):
    def __init__(self):
        super().__init__(
            certification_name="80 PLUS Standard",
            load_levels=[20, 50, 100],
            efficiency_levels=[0.8, 0.8, 0.8]
        )

class EightyPlusBronze(EfficiencyCertification):
    def __init__(self):
        super().__init__(
            certification_name="80 PLUS Bronze",
            load_levels=[20, 50, 100],
            efficiency_levels=[0.82, 0.85, 0.82] 
        )

class EightyPlusSilver(EfficiencyCertification):
    def __init__(self):
        super().__init__(
            certification_name="80 PLUS Silver",
            load_levels=[20, 50, 100],
            efficiency_levels=[0.85, 0.88, 0.85]
        )

class EightyPlusGold(EfficiencyCertification):
    def __init__(self):
        super().__init__(
            certification_name="80 PLUS Gold",
            load_levels=[20, 50, 100],  # Load levels as percentages
            efficiency_levels=[0.87, 0.90, 0.87]  # Efficiency levels as floats (e.g., 0.87 for 87%)
        )

class EightyPlusPlatinum(EfficiencyCertification):
    def __init__(self):
        super().__init__(
            certification_name="80 PLUS Platinum",
            load_levels=[20, 50, 100],
            efficiency_levels=[0.90, 0.92, 0.89]
        )

class EightyPlusTitanium(EfficiencyCertification):
    def __init__(self):
        super().__init__(
            certification_name="80 PLUS Titanium",
            load_levels=[20, 50, 100],
            efficiency_levels=[0.90, 0.92, 0.94]
        )

if __name__ == "__main__":
    pass