def stat_report(result_data: dict) -> None:
    """
    Generates and prints a formatted, color-coded statistical report.
    """
    color_green = '\033[92m'
    color_red = '\033[91m'
    color_reset = '\033[0m'

    func_name = result_data['func_name']
    title = f"Algorithm Performance on {func_name}"
    
    print(f"\n>>> {title}")

    descriptive_stats = result_data["stats"]
    for algo, stats in descriptive_stats.items():
        print(f"\n{algo}:")
        print(f"  Mean fitness:     {stats['mean']:.2e}")
        print(f"  Std deviation:    {stats['std']:.2e}")
        print(f"  Best result:      {stats['best']:.2e}")

    test_used = result_data['test_used']
    print(f"\n>> [{test_used} Test Results]")
    
    stat_name = result_data['stat_name']
    stat_val = result_data['stat_val']
    p_val = result_data['p_val']
    is_significant = result_data['significant']
    alpha = result_data['alpha']

    stat_label = f"{stat_name}:"
    print(f"  {stat_label:<18}{stat_val:.3f}")
    print(f"  {'p-value:':<18}{p_val:.2e}")
    
    if is_significant:
        sig_str = f"{color_green}Yes{color_reset}"
    else:
        sig_str = f"{color_red}No{color_reset}"
    
    print(f"  {'Significant:':<18}{sig_str} (α={alpha})\n")