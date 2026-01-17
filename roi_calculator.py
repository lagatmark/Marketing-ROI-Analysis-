"""
Marketing ROI Calculator
Author: Mark Kipchumba
Date: January 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class MarketingROIAnalyzer:
    def __init__(self, data_path):
        """Initialize with marketing campaign data"""
        self.df = pd.read_csv(data_path)
        self.channel_metrics = {}
        
    def calculate_roi_metrics(self):
        """Calculate all ROI-related metrics"""
        results = {}
        
        for channel in self.df['Channel'].unique():
            channel_data = self.df[self.df['Channel'] == channel]
            
            total_spend = channel_data['Spend'].sum()
            total_revenue = channel_data['Revenue'].sum()
            total_conversions = channel_data['Conversions'].sum()
            
            # Calculate metrics
            roi = ((total_revenue - total_spend) / total_spend) * 100 if total_spend > 0 else 0
            cac = total_spend / total_conversions if total_conversions > 0 else 0
            conversion_rate = (total_conversions / channel_data['Clicks'].sum() * 100) if channel_data['Clicks'].sum() > 0 else 0
            romi = (total_revenue - total_spend) / total_spend if total_spend > 0 else 0
            
            results[channel] = {
                'TotalSpend': total_spend,
                'TotalRevenue': total_revenue,
                'ROI': roi,
                'CAC': cac,
                'ConversionRate': conversion_rate,
                'ROMI': romi,
                'Conversions': total_conversions,
                'Clicks': channel_data['Clicks'].sum(),
                'Impressions': channel_data['Impressions'].sum()
            }
        
        self.channel_metrics = results
        return pd.DataFrame(results).T
    
    def identify_optimization_opportunities(self, budget=100000):
        """Identify budget optimization opportunities"""
        metrics_df = pd.DataFrame(self.channel_metrics).T
        metrics_df = metrics_df.sort_values('ROI', ascending=False)
        
        # Current allocation
        current_allocation = metrics_df['TotalSpend'].copy()
        
        # Optimal allocation (proportional to ROI)
        total_roi = metrics_df['ROI'].sum()
        metrics_df['OptimalAllocation'] = (metrics_df['ROI'] / total_roi) * budget
        
        # Calculate expected improvement
        metrics_df['CurrentRevenue'] = metrics_df['TotalRevenue']
        metrics_df['ExpectedRevenue'] = (metrics_df['OptimalAllocation'] / metrics_df['TotalSpend']) * metrics_df['TotalRevenue']
        metrics_df['RevenueIncrease'] = metrics_df['ExpectedRevenue'] - metrics_df['CurrentRevenue']
        
        return metrics_df
    
    def generate_recommendations(self):
        """Generate business recommendations"""
        metrics_df = self.calculate_roi_metrics()
        
        print("="*60)
        print("MARKETING ROI ANALYSIS REPORT")
        print("="*60)
        
        print("\n📊 CURRENT PERFORMANCE BY CHANNEL:")
        print("-"*60)
        print(f"{'Channel':<15} {'Spend':>10} {'Revenue':>10} {'ROI':>8} {'CAC':>8}")
        print("-"*60)
        
        for channel, metrics in self.channel_metrics.items():
            print(f"{channel:<15} ${metrics['TotalSpend']:>9,.0f} ${metrics['TotalRevenue']:>9,.0f} "
                  f"{metrics['ROI']:>7.0f}% ${metrics['CAC']:>7.0f}")
        
        # Optimization analysis
        print(f"\n🎯 OPTIMIZATION OPPORTUNITIES:")
        print("-"*60)
        
        optimal_df = self.identify_optimization_opportunities()
        
        # Top performers
        top_performers = optimal_df.nlargest(3, 'ROI')
        print("\nTop 3 Performing Channels:")
        for idx, row in top_performers.iterrows():
            print(f"  • {idx}: ROI = {row['ROI']:.0f}%, CAC = ${row['CAC']:.0f}")
        
        # Underperformers
        underperformers = optimal_df.nsmallest(2, 'ROI')
        print("\nChannels Needing Review:")
        for idx, row in underperformers.iterrows():
            print(f"  • {idx}: ROI = {row['ROI']:.0f}%, CAC = ${row['CAC']:.0f}")
        
        # Calculate total impact
        total_increase = optimal_df['RevenueIncrease'].sum()
        print(f"\n💰 POTENTIAL IMPACT:")
        print(f"  Revenue Increase: ${total_increase:,.0f}")
        print(f"  ROI Improvement: {(total_increase / metrics_df['TotalSpend'].sum()) * 100:.1f}%")
        
        print("\n🎯 RECOMMENDED ACTIONS:")
        print("1. Increase budget allocation to high-ROI channels")
        print("2. Reduce spend on underperforming channels by 30%")
        print("3. Implement A/B testing for ad creatives")
        print("4. Review targeting parameters for low-ROI campaigns")
        print("5. Set up weekly performance dashboards")
        
        print("\n📅 NEXT STEPS:")
        print("Week 1-2: Implement budget reallocation")
        print("Week 3-4: Monitor performance and adjust")
        print("Week 5-6: Scale successful strategies")
        print("Week 7-8: Full optimization review")
        
        return optimal_df
    
    def create_visualizations(self):
        """Create marketing performance visualizations"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. ROI by Channel
        channels = list(self.channel_metrics.keys())
        roi_values = [m['ROI'] for m in self.channel_metrics.values()]
        
        axes[0, 0].bar(channels, roi_values, color='lightgreen')
        axes[0, 0].set_title('ROI by Marketing Channel', fontsize=14, fontweight='bold')
        axes[0, 0].set_ylabel('ROI (%)')
        axes[0, 0].tick_params(axis='x', rotation=45)
        
        # 2. CAC by Channel
        cac_values = [m['CAC'] for m in self.channel_metrics.values()]
        axes[0, 1].bar(channels, cac_values, color='lightcoral')
        axes[0, 1].set_title('Customer Acquisition Cost by Channel', fontsize=14, fontweight='bold')
        axes[0, 1].set_ylabel('CAC ($)')
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # 3. Spend vs Revenue Scatter
        spend = [m['TotalSpend'] for m in self.channel_metrics.values()]
        revenue = [m['TotalRevenue'] for m in self.channel_metrics.values()]
        
        axes[1, 0].scatter(spend, revenue, s=200, alpha=0.6)
        for i, channel in enumerate(channels):
            axes[1, 0].annotate(channel, (spend[i], revenue[i]))
        
        # Add trend line
        z = np.polyfit(spend, revenue, 1)
        p = np.poly1d(z)
        axes[1, 0].plot(spend, p(spend), "r--", alpha=0.5)
        
        axes[1, 0].set_title('Spend vs Revenue', fontsize=14, fontweight='bold')
        axes[1, 0].set_xlabel('Total Spend ($)')
        axes[1, 0].set_ylabel('Total Revenue ($)')
        
        # 4. Conversion Rate
        conv_rates = [m['ConversionRate'] for m in self.channel_metrics.values()]
        axes[1, 1].bar(channels, conv_rates, color='skyblue')
        axes[1, 1].set_title('Conversion Rate by Channel', fontsize=14, fontweight='bold')
        axes[1, 1].set_ylabel('Conversion Rate (%)')
        axes[1, 1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig('reports/marketing_performance.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✅ Visualizations saved to 'reports/marketing_performance.png'")

def main():
    """Main execution function"""
    print("🚀 Marketing ROI Analysis Starting...")
    
    # Initialize analyzer
    analyzer = MarketingROIAnalyzer('data/marketing_campaigns.csv')
    
    # Calculate metrics
    print("\n📊 Calculating ROI metrics...")
    metrics = analyzer.calculate_roi_metrics()
    
    # Generate recommendations
    print("\n🎯 Generating recommendations...")
    recommendations = analyzer.generate_recommendations()
    
    # Create visualizations
    print("\n🎨 Creating visualizations...")
    analyzer.create_visualizations()
    
    # Save results
    recommendations.to_csv('reports/roi_analysis_results.csv')
    print("\n✅ Analysis complete! Results saved to:")
    print("   - reports/roi_analysis_results.csv")
    print("   - reports/marketing_performance.png")
    
    return recommendations

if __name__ == "__main__":
    main()
