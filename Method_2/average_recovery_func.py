from create_equity_curve import unit_equity_df, equity_df
import numpy as np
def analyze_drawdowns_and_recovery(equity_curve = equity_df):
    high_water_mark = float('-inf')
    in_drawdown = False
    
    peak_day = 0
    peak_value = float('-inf')
    
    current_drawdown = {}
    completed_drawdowns = []

    for day, current_value in enumerate(equity_curve['equity']):
        
        if current_value >= high_water_mark:
            
            if in_drawdown:
                current_drawdown['recovery_day'] = day
                
                current_drawdown['drawdown_length_days'] = (current_drawdown['trough_day'] - 
                                                            current_drawdown['peak_day'])
                
                current_drawdown['recovery_period_days'] = (current_drawdown['recovery_day'] - 
                                                             current_drawdown['trough_day'])
                
                current_drawdown['underwater_period_days'] = (current_drawdown['recovery_day'] - 
                                                              current_drawdown['peak_day'])
                
                completed_drawdowns.append(current_drawdown)
                
                in_drawdown = False
                current_drawdown = {}

            high_water_mark = current_value
            peak_day = day
            peak_value = current_value
        
        elif current_value < high_water_mark:
            
            if not in_drawdown:
                in_drawdown = True
                current_drawdown = {
                    'peak_day': peak_day,
                    'peak_value': peak_value,
                    'trough_day': day,
                    'trough_value': current_value
                }
            
            else:
                if current_value < current_drawdown['trough_value']:
                    current_drawdown['trough_day'] = day
                    current_drawdown['trough_value'] = current_value

    total_recovery_days = 0
    num_recoveries = len(completed_drawdowns)
    recovery_period_list = []
    if num_recoveries > 0:

        for dd in completed_drawdowns:
            recovery_period_list.append(dd['recovery_period_days'])
        average_recovery_period = np.mean(recovery_period_list)
        median_recovery_period = np.median(recovery_period_list)
    #return completed_drawdowns, average_recovery_period, median_recovery_period
    return completed_drawdowns

# --- Example Usage ---

#all_events, avg_recovery, median_recovery_period = analyze_drawdowns_and_recovery()
all_events = analyze_drawdowns_and_recovery()

#formatting for proper display
"""
print("--- DETAILED DRAWDOWN EVENTS ---")
for i, event in enumerate(all_events):
    print(f"\n--- Event {i+1} ---")
    print(f"Peak:           {event['peak_value']} on day {event['peak_day']}")
    print(f"Trough:         {event['trough_value']} on day {event['trough_day']}")
    print(f"Recovered on:   day {event['recovery_day']}")
    print(f"Recovery Period: {event['recovery_period_days']} days")
    print(f"Max Drawdown:   {(event['trough_value'] / event['peak_value'] - 1):.2%}")

print("\n" + "="*40)
print(f"FINAL RESULT:")
print(f"Found {len(all_events)} completed drawdown events.")
print(f"The Average Recovery Period is: {avg_recovery:.2f} days")
print("="*40)
"""
recovery_period_list = []
underwater_period_list = []
for event in all_events:
    recovery_period_list.append(event['recovery_period_days'])
    underwater_period_list.append(event['underwater_period_days'])

#print(all_events)
if __name__ == "__main__":
    print(f"Recovery Period List: {recovery_period_list}")
    print(f"Underwater Period List: {underwater_period_list}")
    print(f"Average recovery period: {np.mean(recovery_period_list)}")
    print(f"Median recovery period: {np.median(recovery_period_list)}")
    print(f"Average Time Underwater (Drawdown Duration) : {np.mean(underwater_period_list)}")
    print(f"Median Time Underwater (Drawdown Duration) : {np.median(underwater_period_list)}")
    print(f"Total Completed Drawdowns: {len(recovery_period_list)}")