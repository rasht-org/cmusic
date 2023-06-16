class Project:
    
    name: str
    # Number of frames to shift each lyric line
    frameShift: int
    # Number of frames per second
    fps: int
    # Start from frame
    start_frame: int
    # Final frame
    end_frame: int
    # List of prompts extracted from lyric
    prompts: map
    # Number of frames to shift lyric timing
    prompt_padding: int
    
    def __init__(self) -> None:
        self.fps = 15
        self.frameShift = -5
        self.start_frame = 0
        self.end_frame = -1
        self.prompts = {}
        
        
    def transform(self, prompts):
        transformed_prompts = {}
        for (index, value) in enumerate(prompts):
            time = round(float(value) * self.fps) + self.frameShift
            if time < 0: time = 0
            transformed_prompts[time] = prompts[value]
        return transformed_prompts