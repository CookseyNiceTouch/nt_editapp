from transcriptanalysis.videoanalyzer import main as videoanalyzer_main

def main():
    """Main entry point for the transcript analysis package."""
    # By default, we delegate to the videoanalyzer module
    videoanalyzer_main()


if __name__ == "__main__":
    main()
