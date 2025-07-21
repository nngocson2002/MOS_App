import re
import os
import json
import pandas as pd
import gradio as gr
from datetime import datetime
from display_text import DESCRIPTIONS


class MOSApp:

    MOS_SCORES = {
        "1 - Bad": 1,
        "1.5": 1.5,
        "2 - Poor": 2,
        "2.5": 2.5,
        "3 - Fair": 3,
        "3.5": 3.5,
        "4 - Good": 4,
        "4.5": 4.5,
        "5 - Excellent": 5
    }

    def __init__(self, dirpath: str, outdir: str, progress_dir: str):
        csv_files = os.listdir(dirpath)
        self.dfs = [pd.read_csv(os.path.join(dirpath, f)) for f in csv_files]
        self.current_files = None
        self.current_transcripts = None
        self.current_models = None
        self.current_gt = None
        self.id_to_take = 0
        self.outdir = outdir
        self.rev_mos = {v: k for k, v in self.MOS_SCORES.items()}
        os.makedirs(outdir, exist_ok=True)
        self.progress_dir = progress_dir
        os.makedirs(progress_dir, exist_ok=True)

    def save_state(self, state):
        """Save the current state to a JSON file using tester_id as filename."""
        if state.get("tester_id"):
            progress_path = os.path.join(self.progress_dir, f"{state['tester_id']}.json")
            with open(progress_path, "w") as f:
                json.dump(state, f)
        return

    def load_state(self, tester_id):
        """Load the state for a given tester_id if it exists."""
        progress_path = os.path.join(self.progress_dir, f"{tester_id}.json")
        if os.path.exists(progress_path):
            with open(progress_path, "r") as f:
                return json.load(f)
        return None

    def get_current_info(self):
        if self.id_to_take >= len(self.dfs):
            self.id_to_take = 0
        self.current_files = self.dfs[self.id_to_take]["filepath"].tolist()
        self.current_transcripts = self.dfs[self.id_to_take]["transcript"].tolist()
        self.current_models = self.dfs[self.id_to_take]["model"].tolist()
        self.current_gt = self.dfs[self.id_to_take]["gt"].tolist()
        self.id_to_take += 1
        return (
            self.current_files,
            self.current_transcripts,
            self.current_models,
            self.current_gt,
        )

    def initialize_state(self):
        return {
            "index": 0,
            "selected_naturalness_MOS": [],
            "selected_intelligibility_MOS": [],
            "selected_similarity_MOS": [],
            "tester_id": "",
            "current_files": None,
            "current_transcripts": None,
            "current_models": None,
            "current_gt": None,
        }

    def submit_options(self, naturalness, intelligibility, similarity, state):

        # Warn if any score is not selected
        if naturalness is None:
            gr.Warning("Please rate NATURALNESS before submitting.", duration=5)
            return (
                state["current_files"][state["index"]],
                naturalness,
                intelligibility,
                similarity,
                state,
                state["current_transcripts"][state["index"]],
                state["current_gt"][state["index"]],
                gr.update(),
                gr.update(),
                gr.update(),
            )
        if intelligibility is None:
            gr.Warning("Please rate INTELLIGIBILITY before submitting.", duration=5)
            return (
                state["current_files"][state["index"]],
                naturalness,
                intelligibility,
                similarity,
                state,
                state["current_transcripts"][state["index"]],
                state["current_gt"][state["index"]],
                gr.update(),
                gr.update(),
                gr.update(),
            )
        if similarity is None:
            gr.Warning("Please rate SIMILARITY before submitting.", duration=5)
            return (
                state["current_files"][state["index"]],
                naturalness,
                intelligibility,
                similarity,
                state,
                state["current_transcripts"][state["index"]],
                state["current_gt"][state["index"]],
                gr.update(),
                gr.update(),
                gr.update(),
            )

        current_files = state["current_files"]
        if not current_files:
            return (
                None,
                None,
                None,
                None,
                state,
                "",
                None,
                gr.update(),
                gr.update(),
                gr.update(),
            )

        submitted_count = len(state["selected_naturalness_MOS"])

        # If the current index is less than submitted_count, we are editing a past evaluation.
        if state["index"] < submitted_count:
            state["selected_naturalness_MOS"][state["index"]] = self.MOS_SCORES[naturalness]
            state["selected_intelligibility_MOS"][state["index"]] = self.MOS_SCORES[intelligibility]
            state["selected_similarity_MOS"][state["index"]] = self.MOS_SCORES[similarity]
            state["index"] += 1
            audio = current_files[state["index"]]
            transcript = state["current_transcripts"][state["index"]]
            gt = state["current_gt"][state["index"]]
            self.save_state(state)
        elif state["index"] == submitted_count:
            # New evaluation: append the scores.
            state["selected_naturalness_MOS"].append(self.MOS_SCORES[naturalness])
            state["selected_intelligibility_MOS"].append(self.MOS_SCORES[intelligibility])
            state["selected_similarity_MOS"].append(self.MOS_SCORES[similarity])
            state["index"] += 1  # Move to the next evaluation.
            if state["index"] < len(current_files):
                audio = current_files[state["index"]]
                transcript = state["current_transcripts"][state["index"]]
                gt = state["current_gt"][state["index"]]
            else:
                audio, transcript, gt = None, "", None
            self.save_state(state)
        else:
            audio, transcript, gt = None, "", None

        # If the user has finished all evaluations, save CSV.
        if state["index"] >= len(current_files):
            results_df = pd.DataFrame({
                "filepath": state["current_files"],
                "model": state["current_models"],
                "Natural-MOS": state["selected_naturalness_MOS"],
                "Intelligibility-MOS": state["selected_intelligibility_MOS"],
                "Similarity-MOS": state["selected_similarity_MOS"],
            })
            csv_path = os.path.join(self.outdir, f"{state['tester_id']}.csv")
            results_df.to_csv(csv_path, index=False)
            gr.Success("Thank you for your feedback! Evaluation finished.", duration=5)
            # Disable navigation buttons when finished.
            return (
                None,
                None,
                None,
                None,
                state,
                "",
                None,
                gr.update(value=state["index"]),
                gr.update(interactive=False),
                gr.update(interactive=False),
            )
        else:
            # Update navigation buttons
            back_update = gr.update(interactive=True) if state["index"] > 0 \
                else gr.update(interactive=False)
            next_update = gr.update(interactive=True) if state["index"] < submitted_count \
                else gr.update(interactive=False)
            return (
                audio,
                None,
                None,
                None,
                state,
                transcript,
                gt,
                gr.update(value=state["index"] + 1),
                back_update,
                next_update,
            )

    def set_tester_id(self, id, state):

        # Try to load an existing state
        loaded_state = self.load_state(id)

        if loaded_state is not None:
            # Use the loaded state and provide the next audio sample based on saved index.
            state = loaded_state
            id_display_text = f"## Welcome back! Your ID: {state['tester_id']}"
        else:
            # No saved state; initialize a new one.
            (
                state["current_files"],
                state["current_transcripts"],
                state["current_models"],
                state["current_gt"],
            ) = self.get_current_info()
            state["tester_id"] = id
            state["index"] = 0
            # Save the new state
            self.save_state(state)
            id_display_text = f"## Your ID: {state['tester_id']}"

        return (
            id_display_text,
            state,
            state["current_files"][state["index"]],
            state["current_transcripts"][state["index"]],
            state["current_gt"][state["index"]],
            gr.update(visible=False, interactive=False),
            gr.update(visible=False, interactive=False),
            gr.update(interactive=False),
            gr.update(interactive=True),
            gr.update(interactive=True),
            gr.update(interactive=True),
            gr.update(value=state["index"] + 1),
        )

    def go_back(self, state):
        submitted_count = len(state["selected_naturalness_MOS"])
        if state["index"] > 0:
            state["index"] -= 1

        # Load the previously submitted scores
        if state["index"] < submitted_count:
            naturalness = self.rev_mos[state["selected_naturalness_MOS"][state["index"]]]
            intelligibility = self.rev_mos[state["selected_intelligibility_MOS"][state["index"]]]
            similarity = self.rev_mos[state["selected_similarity_MOS"][state["index"]]]
        else:
            naturalness, intelligibility, similarity = None, None, None

        back_update = gr.update(interactive=True) if state["index"] > 0 \
            else gr.update(interactive=False)
        next_update = gr.update(interactive=True) if state["index"] < submitted_count \
            else gr.update(interactive=False)

        return (
            state["current_files"][state["index"]],
            state["current_transcripts"][state["index"]],
            state["current_gt"][state["index"]],
            naturalness,
            intelligibility,
            similarity,
            state,
            gr.update(value=state["index"] + 1),
            back_update,
            next_update,
        )

    def go_next(self, state):
        submitted_count = len(state["selected_naturalness_MOS"])
        if state["index"] < submitted_count:
            state["index"] += 1

        # Load the next audio sample
        if state["index"] < submitted_count:
            naturalness = self.rev_mos.get(state["selected_naturalness_MOS"][state["index"]], None)
            intelligibility = self.rev_mos.get(state["selected_intelligibility_MOS"][state["index"]], None)
            similarity = self.rev_mos.get(state["selected_similarity_MOS"][state["index"]], None)
        else:
            naturalness, intelligibility, similarity = None, None, None

        back_update = gr.update(interactive=True) if state["index"] > 0 \
            else gr.update(interactive=False)
        next_update = gr.update(interactive=True) if state["index"] < submitted_count \
            else gr.update(interactive=False)

        return (
            state["current_files"][state["index"]],
            state["current_transcripts"][state["index"]],
            state["current_gt"][state["index"]],
            naturalness,
            intelligibility,
            similarity,
            state,
            gr.update(value=state["index"] + 1),
            back_update,
            next_update,
        )

    def toggle_language(self, language_toggle):
        texts = DESCRIPTIONS["English"] if language_toggle else DESCRIPTIONS["Vietnamese"]
        return (
            gr.update(label=texts["language_toggle"]),
            gr.update(value=texts["sidebar"]),
            gr.update(value=texts["naturalness_guidelines"]),
            gr.update(value=texts["intelligibility_guidelines"]),
            gr.update(value=texts["similarity_guidelines"]),
            gr.update(value=texts["naturalness_table"]),
            gr.update(value=texts["intelligibility_table"]),
            gr.update(value=texts["similarity_table"]),
        )

    def check_submit_button(self, naturalness, intelligibility, similarity):
        if naturalness is not None and intelligibility is not None and similarity is not None:
            return gr.update(interactive=True)
        else:
            return gr.update(interactive=False)

    def create_interface(self):

        with gr.Blocks(theme='davehornik/Tealy', fill_width=True, title="MOS Survey") as demo:
            def hello():
                gr.Info("Hello! Please read the sidebar instructions carefully before starting the survey.")

            demo.load(hello, inputs=[], outputs=[])

            with gr.Sidebar(open=True, width=350):
                sidebar_instructions = gr.Markdown(DESCRIPTIONS["Vietnamese"]["sidebar"])

            state = gr.State(self.initialize_state())

            with gr.Row():
                with gr.Column(scale=5):
                    gr.Markdown("# Mean Opinion Score (MOS) Survey")
                with gr.Column(scale=1):
                    language_toggle = gr.Checkbox(
                        label=DESCRIPTIONS["Vietnamese"]["language_toggle"],
                        value=False,
                        interactive=True,
                    )

            gr.Markdown("------")

            gr.Markdown("## Step 1. Enter your ID. If you have participated before, your progress will be restored.")

            with gr.Row():
                tester_id_input = gr.Textbox(
                    label="Enter Your ID", interactive=True
                )
                set_id_button = gr.Button("Set ID", interactive=False, variant="primary")
                id_display = gr.Markdown()

            # Enable/disable the Set ID button based on input.
            def toggle_set_id_button(tester_id):

                def check_valid_id(tester_id):
                    id = tester_id.strip()
                    if not id:
                        gr.Warning("Spaces are not allowed.", duration=5)
                        return False
                    if re.match(r"^[a-zA-Z0-9]+$", id):
                        return True
                    else:
                        gr.Warning("Only alphanumeric characters are allowed.", duration=5)
                        return False

                return gr.update(interactive=check_valid_id(tester_id))

            tester_id_input.change(
                toggle_set_id_button,
                inputs=[tester_id_input],
                outputs=[set_id_button],
            )

            gr.Markdown("------")
            gr.Markdown("## Step 2. Listen carefully to the following audio: ")

            with gr.Row(equal_height=True):
                with gr.Column(scale=2):
                    display_audio = gr.Audio(None, type="filepath", label="Synthesized Voice")

                with gr.Column(scale=2):
                    gt_display_audio = gr.Audio(None, type="filepath", label="Reference Voice")

                with gr.Column(scale=1):
                    progress_bar = gr.Slider(minimum=1, maximum=len(self.dfs[0]), value=0, label="Progress", interactive=False)
                    transcript_box = gr.Textbox(label="Ground-truth Transcript", interactive=False)

            gr.Markdown("------")

            gr.Markdown(
                "## Step 3. Answer the following questions basing on the audio you hear.",
                max_height=100
            )

            with gr.Row(equal_height=True):

                with gr.Column():

                    gr.Markdown("### How natural is the above audio?")

                    with gr.Accordion("Evaluation Guidelines (Click to collapse/expand)", open=True):
                        naturalness_guide = gr.Markdown(
                            DESCRIPTIONS["Vietnamese"]["naturalness_guidelines"], max_height=100
                        )

                    naturalness_table = gr.Markdown(DESCRIPTIONS["Vietnamese"]["naturalness_table"])

                    naturalness = gr.Radio(
                        choices=[
                            "1 - Bad",
                            "1.5",
                            "2 - Poor",
                            "2.5",
                            "3 - Fair",
                            "3.5",
                            "4 - Good",
                            "4.5",
                            "5 - Excellent"
                        ],
                        value=None,
                        label="Naturalness Score",
                        interactive=False,
                    )

                with gr.Column():
                    gr.Markdown("### How would you rate the intelligibility of the voice?")
                    with gr.Accordion("Evaluation Guidelines (Click to collapse/expand)", open=True):
                        intelligibility_guide = gr.Markdown(
                            DESCRIPTIONS["Vietnamese"]["intelligibility_guidelines"], max_height=100
                        )

                    intelligibility_table = gr.Markdown(
                        DESCRIPTIONS["Vietnamese"]["intelligibility_table"]
                    )

                    intelligibility = gr.Radio(
                        choices=[
                            "1 - Bad",
                            "1.5",
                            "2 - Poor",
                            "2.5",
                            "3 - Fair",
                            "3.5",
                            "4 - Good",
                            "4.5",
                            "5 - Excellent"
                        ],
                        value=None,
                        label="Intelligibility Score",
                        interactive=False,
                    )

                with gr.Column():
                    gr.Markdown("### How similar are the speakers of the above two audio samples?")
                    with gr.Accordion("Evaluation Guidelines (Click to collapse/expand)", open=True):
                        similarity_guide = gr.Markdown(
                            DESCRIPTIONS["Vietnamese"]["similarity_guidelines"], max_height=100
                        )

                    similarity_table = gr.Markdown(DESCRIPTIONS["Vietnamese"]["similarity_table"])

                    similarity = gr.Radio(
                        choices=[
                            "1 - Bad",
                            "1.5",
                            "2 - Poor",
                            "2.5",
                            "3 - Fair",
                            "3.5",
                            "4 - Good",
                            "4.5",
                            "5 - Excellent"
                        ],
                        value=None,
                        label="Similarity Score",
                        interactive=False,
                    )

            with gr.Row():
                with gr.Column(scale=1):
                    back_btn = gr.Button("Back", interactive=False, variant="secondary")
                with gr.Column(scale=2):
                    submit_btn = gr.Button("Submit", interactive=False, variant="primary")
                with gr.Column(scale=1):
                    next_btn = gr.Button("Next", interactive=False, variant="secondary")

            naturalness.change(
                self.check_submit_button,
                inputs=[naturalness, intelligibility, similarity],
                outputs=[submit_btn],
            )
            intelligibility.change(
                self.check_submit_button,
                inputs=[naturalness, intelligibility, similarity],
                outputs=[submit_btn],
            )
            similarity.change(
                self.check_submit_button,
                inputs=[naturalness, intelligibility, similarity],
                outputs=[submit_btn],
            )

            # Navigation callbacks.
            back_btn.click(
                self.go_back,
                inputs=[state],
                outputs=[
                    display_audio,
                    transcript_box,
                    gt_display_audio,
                    naturalness,
                    intelligibility,
                    similarity,
                    state,
                    progress_bar,
                    back_btn,
                    next_btn,
                ],
            )
            next_btn.click(
                self.go_next,
                inputs=[state],
                outputs=[
                    display_audio,
                    transcript_box,
                    gt_display_audio,
                    naturalness,
                    intelligibility,
                    similarity,
                    state,
                    progress_bar,
                    back_btn,
                    next_btn,
                ],
            )

            language_toggle.change(
                self.toggle_language,
                inputs=[language_toggle],
                outputs=[
                    language_toggle,
                    sidebar_instructions,
                    naturalness_guide,
                    intelligibility_guide,
                    similarity_guide,
                    naturalness_table,
                    intelligibility_table,
                    similarity_table,
                ]
            )
            set_id_button.click(
                self.set_tester_id,
                inputs=[tester_id_input, state],
                outputs=[
                    id_display,
                    state,
                    display_audio,
                    transcript_box,
                    gt_display_audio,
                    tester_id_input,
                    set_id_button,
                    submit_btn,
                    naturalness,
                    intelligibility,
                    similarity,
                    progress_bar,
                ],
            )
            submit_btn.click(
                self.submit_options,
                inputs=[naturalness, intelligibility, similarity, state],
                outputs=[
                    display_audio,
                    naturalness,
                    intelligibility,
                    similarity,
                    state,
                    transcript_box,
                    gt_display_audio,
                    progress_bar,
                    back_btn,
                    next_btn,
                ],
            )

        return demo


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    current_date = datetime.now().strftime("%Y%m%d")
    app = MOSApp(
        dirpath="./samples/data",   # change as you need
        outdir=f"./results/{current_date}",
        progress_dir=f"./progress/{current_date}",
    )
    demo = app.create_interface()
    demo.launch(share=True)
    # demo.launch(server_name="0.0.0.0", server_port=port)
