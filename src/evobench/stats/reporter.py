def stat_report(result_data: dict) -> None:
    """
    Generates and prints a formatted, color-coded statistical report.
    Includes post-hoc test results when available.
    """
    color_green = '\033[92m'
    color_red = '\033[91m'
    color_yellow = '\033[93m'
    color_blue = '\033[94m'
    color_cyan = '\033[96m'
    color_bold = '\033[1m'
    color_reset = '\033[0m'

    func_name = result_data['func_name']
    title = f"Algorithm Performance on {func_name}"
    
    print(f"\n>>> {color_bold}{title}{color_reset}")

    # Descriptive Statistics
    descriptive_stats = result_data["stats"]
    print(f"\n{color_cyan}[Descriptive Statistics]{color_reset}")
    for algo, stats in descriptive_stats.items():
        print(f"\n{color_bold}{algo}{color_reset}:")
        print(f"  Mean fitness:     {stats['mean']:.2e}")
        print(f"  Std deviation:    {stats['std']:.2e}")
        print(f"  Best result:      {stats['best']:.2e}")

    # Normality Test Results
    if "normality_results" in result_data:
        print(f"\n{color_cyan}[Normality Test Results (Shapiro-Wilk)]{color_reset}")
        for algo, is_normal in result_data["normality_results"].items():
            status = f"{color_green}Normal{color_reset}" if is_normal else f"{color_red}Non-normal{color_reset}"
            print(f"  {algo:<15}: {status}")

    # Global Test Results
    test_used = result_data['test_used']
    print(f"\n{color_cyan}[{test_used} Test Results]{color_reset}")
    
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
        conclusion = f"{color_green}There ARE significant differences between algorithms{color_reset}"
    else:
        sig_str = f"{color_red}No{color_reset}"
        conclusion = f"{color_yellow}No significant differences detected between algorithms{color_reset}"
    
    print(f"  {'Significant:':<18}{sig_str} (α={alpha})")
    print(f"\n{conclusion}")

    # Post-hoc Test Results
    if is_significant and result_data.get("post_hoc_results"):
        post_hoc = result_data["post_hoc_results"]
        print(f"\n{color_cyan}[{post_hoc['test_type']}]{color_reset}")
        print(f"  Correction method: {post_hoc['correction']}")
        
        # Show pairwise comparisons in a formatted table
        print(f"\n{color_bold}{'Algorithm 1':<15} {'Algorithm 2':<15} {'Different?':<15} {'p-value':<12}{color_reset}")
        print(f"  {'-'*60}")
        
        for comp in post_hoc["comparisons"]:
            algo1, algo2 = comp["pair"]
            is_sig = comp["significant"]
            p_val = comp["p_value"]
            
            if is_sig:
                diff_str = f"{color_green} YES{color_reset}"
                winner = f"{color_bold}BETTER:{color_reset}"
                
                # Determine which is better based on mean difference (lower is better for minimization)
                if "mean_rank_diff" in comp:
                    # For Dunn's test (Kruskal-Wallis follow-up)
                    mean1 = result_data["stats"][algo1]["mean"]
                    mean2 = result_data["stats"][algo2]["mean"]
                    better_algo = algo1 if mean1 < mean2 else algo2
                    print(f"  {algo1:<15} {algo2:<15} {diff_str:<15} {p_val:<12} {winner} {color_green}{better_algo}{color_reset}")
                else:
                    # For Tukey HSD
                    meandiff = comp["meandiff"]
                    better_algo = algo1 if meandiff < 0 else algo2
                    print(f"  {algo1:<15} {algo2:<15} {diff_str:<15} {p_val:<12} {winner} {color_green}{better_algo}{color_reset}")
            else:
                diff_str = f"{color_yellow} NO{color_reset}"
                print(f"  {algo1:<15} {algo2:<15} {diff_str:<15} {p_val:<12}")
        
        # Summary Table
        print(f"\n{color_cyan}[Algorithm Ranking by Mean Fitness]{color_reset}")
        if "group_means" in post_hoc:
            # Tukey HSD
            means_dict = post_hoc["group_means"]
        else:
            # Dunn's test - use original means
            means_dict = {name: result_data["stats"][name]["mean"] for name in result_data["stats"]}
        
        sorted_algos = sorted(means_dict.items(), key=lambda x: x[1])
        for rank, (algo, mean) in enumerate(sorted_algos, 1):
            medal = "1" if rank == 1 else "2" if rank == 2 else "3" if rank == 3 else f"  {rank}."
            print(f"  {medal} {algo:<10} -> {mean:.2e}")

    print()  # Final newline