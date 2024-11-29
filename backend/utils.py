def revert_stage_or_step(current_stage, current_main_stage_step):
    reverted_stage = ""
    reverted_main_stage_step = ""
    
    if current_stage == "main":
        if current_main_stage_step == "coding":
            reverted_stage = "thought_process"
            reverted_main_stage_step = ""
        else:
            revert_step_map = {
                "debugging": "coding",
                "algorithmic_analysis": "debugging",
            }
            reverted_stage = "main"
            reverted_main_stage_step = revert_step_map[current_main_stage_step]
    elif current_stage == "assessment":
        reverted_stage = "main"
        reverted_main_stage_step = "algorithmic_analysis"

    return reverted_stage, reverted_main_stage_step
