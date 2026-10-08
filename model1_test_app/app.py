"""Standalone Testing Application for Model 1 Plant/Crop Identification.

Supports:
1. Single-image classification (EfficientNet-B2)
2. Video plant/crop identification with 16-24 uniform frame extraction,
   adaptive quality filtering, Model 1 inference on EVERY selected frame,
   mean probability aggregation, and complete visual review of all frames.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import streamlit as st
from PIL import Image

from model1_test_app.inference import load_model, predict_image
try:
    from model1_test_app.video_inference import (
        MAX_TARGET_FRAMES,
        MIN_TARGET_FRAMES,
        TARGET_FRAMES_DEFAULT,
        predict_video,
    )
except ImportError:
    from model1_test_app.video_inference import predict_video
    TARGET_FRAMES_DEFAULT = 24
    MIN_TARGET_FRAMES = 16
    MAX_TARGET_FRAMES = 24
from video.frame_extractor import (
    EmptyVideoError,
    InvalidVideoError,
    SUPPORTED_VIDEO_EXTENSIONS,
)

# Supported image and video extensions
SUPPORTED_IMAGE_EXTS = ["jpg", "jpeg", "png", "webp", "bmp"]
SUPPORTED_VIDEO_EXTS = [ext.lstrip(".") for ext in sorted(SUPPORTED_VIDEO_EXTENSIONS)]


@st.cache_resource(show_spinner="Loading Model 1 (EfficientNet-B2)...")
def get_cached_model():
    """Load and cache Model 1 checkpoint once in memory."""
    return load_model()


def main():
    st.set_page_config(
        page_title="Model 1 | Plant & Crop Identification",
        page_icon="🌱",
        layout="wide",
    )

    # Header
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 20px;">
            <h1 style="color: #22c55e; margin-bottom: 4px; font-weight: 800;">🌱 PLANT / CROP IDENTIFICATION</h1>
            <p style="color: #94a3b8; font-size: 1.1rem; margin-top: 0;">
                Model 1 Testing Suite (EfficientNet-B2 &bull; 22-Class Transfer Learning)
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Initialize model
    try:
        model, idx_to_class, class_to_idx, device, device_name = get_cached_model()
    except Exception as exc:
        st.error(f"❌ Failed to load Model 1 checkpoint: {exc}")
        st.stop()

    # System Status Bar
    col_status1, col_status2, col_status3 = st.columns([1, 1, 1])
    with col_status1:
        st.markdown(f"**⚡ Device:** `{device_name}`")
    with col_status2:
        st.markdown(f"**🧠 Architecture:** `EfficientNet-B2`")
    with col_status3:
        st.markdown(f"**🏷 Classes:** `{len(idx_to_class)} Target Crops`")

    st.markdown("---")

    # Input Tabs
    tab_image, tab_video = st.tabs(["🖼 IMAGE INFERENCE", "🎥 VIDEO INFERENCE"])

    # ----------------------------------------------------
    # TAB 1: IMAGE INFERENCE
    # ----------------------------------------------------
    with tab_image:
        st.subheader("Single Image Classification")
        st.caption("Upload a crop, flower, or leaf image to identify the plant species.")

        uploaded_img = st.file_uploader(
            "Select an image file:",
            type=SUPPORTED_IMAGE_EXTS,
            key="img_uploader",
            help="Supported: JPG, JPEG, PNG, WEBP, BMP",
        )

        if uploaded_img is not None:
            col_img_view, col_img_res = st.columns([1, 1], gap="large")

            with col_img_view:
                st.markdown("##### Uploaded Specimen")
                try:
                    pil_img = Image.open(uploaded_img)
                    st.image(pil_img, use_container_width=True)
                except Exception as exc:
                    st.error(f"Could not open image file: {exc}")
                    pil_img = None

            with col_img_res:
                if pil_img is not None:
                    try:
                        with st.spinner("Analyzing plant specimen..."):
                            result = predict_image(
                                pil_img, model, idx_to_class, device, top_k=3
                            )

                        status = result.get("status", "valid")
                        if status == "blurry":
                            st.markdown(
                                f"""
                                <div style="background-color: #451a03; border: 2px solid #f59e0b; border-radius: 12px; padding: 22px; margin-bottom: 20px;">
                                    <div style="color: #fde68a; font-size: 0.95rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">
                                        ⚠️ Image Quality Warning
                                    </div>
                                    <div style="color: #ffffff; font-size: 2.3rem; font-weight: 800; margin: 6px 0;">
                                        BLURRY
                                    </div>
                                    <div style="color: #fcd34d; font-size: 1.1rem; font-weight: 500;">
                                        {result.get('reason', 'Image lacks sharpness or focus.')}
                                    </div>
                                    <div style="color: #cbd5e1; font-size: 0.9rem; margin-top: 10px;">
                                        Please upload a clear, focused image of the plant or leaf.
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                        elif status == "unknown":
                            st.markdown(
                                f"""
                                <div style="background-color: #1e293b; border: 2px solid #64748b; border-radius: 12px; padding: 22px; margin-bottom: 20px;">
                                    <div style="color: #cbd5e1; font-size: 0.95rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">
                                        🔍 Specimen Recognition
                                    </div>
                                    <div style="color: #ffffff; font-size: 2.3rem; font-weight: 800; margin: 6px 0;">
                                        UNKNOWN
                                    </div>
                                    <div style="color: #94a3b8; font-size: 1.1rem; font-weight: 500;">
                                        {result.get('reason', 'No recognizable plant, flower, or leaf visible.')}
                                    </div>
                                    <div style="color: #64748b; font-size: 0.9rem; margin-top: 10px;">
                                        The image does not contain a discernible crop specimen from the 22 supported plant classes.
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                        else:
                            # Top-1 Result Card
                            st.markdown(
                                f"""
                                <div style="background-color: #064e3b; border: 2px solid #10b981; border-radius: 12px; padding: 22px; margin-bottom: 20px;">
                                    <div style="color: #6ee7b7; font-size: 0.95rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">
                                        Predicted Plant / Crop
                                    </div>
                                    <div style="color: #ffffff; font-size: 2.3rem; font-weight: 800; margin: 6px 0;">
                                        {result['predicted_label']}
                                    </div>
                                    <div style="color: #a7f3d0; font-size: 1.25rem; font-weight: 600;">
                                        Confidence: <span style="color:#ffffff;">{result['percentage']}</span>
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                            # Top-3 Predictions Breakdown
                            st.markdown("##### 📊 Top-3 Probabilities")
                            for item in result["top_k"]:
                                col_label, col_val = st.columns([3, 1])
                                with col_label:
                                    st.write(f"**{item['rank']}. {item['label']}**")
                                with col_val:
                                    st.write(f"`{item['percentage']}`")
                                st.progress(item["confidence"])

                    except Exception as exc:
                        st.error(f"Inference error: {exc}")

    # ----------------------------------------------------
    # TAB 2: VIDEO INFERENCE
    # ----------------------------------------------------
    with tab_video:
        st.subheader("Video Plant/Crop Identification")
        st.caption(
            "Upload a video of crops or plants. The system uniformly samples 16–24 frames across the duration, "
            "evaluates each through Model 1, and calculates an aggregated prediction."
        )

        col_vid_left, col_vid_ctrl = st.columns([1, 1], gap="large")

        with col_vid_left:
            uploaded_vid = st.file_uploader(
                "Select a video file:",
                type=SUPPORTED_VIDEO_EXTS,
                key="vid_uploader",
                help=f"Supported: {', '.join(SUPPORTED_VIDEO_EXTS)}",
            )

        with col_vid_ctrl:
            st.markdown("##### Video Sampling & Quality Options")
            target_frames_choice = st.slider(
                "Target Frames for Inference (16–24 frames):",
                min_value=MIN_TARGET_FRAMES,
                max_value=MAX_TARGET_FRAMES,
                value=TARGET_FRAMES_DEFAULT,
                step=1,
                help="Default: 24 frames. Uniformly distributed across the video (0% to 100%).",
            )
            st.caption(
                f"🎯 **Target:** {target_frames_choice} frames uniformly sampled across video with automatic quality replenishment."
            )
            use_quality_filter = st.checkbox(
                "Enable Quality Filter (Automatically discards dark / blurry frames and replenishes with usable ones)",
                value=True,
            )

        if uploaded_vid is not None:
            st.markdown("---")
            v_col1, v_col2 = st.columns([1, 1])
            with v_col1:
                st.markdown("##### Video Preview")
                st.video(uploaded_vid)
            with v_col2:
                st.write(f"**Filename:** `{uploaded_vid.name}`")
                st.write(f"**Filesize:** `{uploaded_vid.size / (1024*1024):.2f} MB`")
                st.write(f"**Target Frames:** `{target_frames_choice} frames`")

                run_video_btn = st.button(
                    f"🚀 Analyze Video ({target_frames_choice} Frames)",
                    type="primary",
                    use_container_width=True,
                )

            if run_video_btn:
                # Save uploaded video to temporary file
                ext = Path(uploaded_vid.name).suffix.lower()
                with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp_f:
                    tmp_f.write(uploaded_vid.getvalue())
                    tmp_video_path = Path(tmp_f.name)

                try:
                    with st.spinner(f"Extracting {target_frames_choice} frames, evaluating with Model 1, and aggregating..."):
                        v_result = predict_video(
                            video_path=tmp_video_path,
                            model=model,
                            idx_to_class=idx_to_class,
                            device=device,
                            target_frames=target_frames_choice,
                            min_target=MIN_TARGET_FRAMES,
                            quality_filter=use_quality_filter,
                            top_k=3,
                        )

                    final_pred = v_result["final_prediction"]
                    final_status = final_pred.get("status", "valid")

                    st.markdown("---")
                    st.markdown("### 🏆 FINAL VIDEO PREDICTION")

                    # Prominent Final Result Card
                    res_col1, res_col2 = st.columns([1, 1])
                    with res_col1:
                        if final_status == "blurry":
                            st.markdown(
                                f"""
                                <div style="background-color: #451a03; border: 2px solid #f59e0b; border-radius: 12px; padding: 24px; margin-bottom: 20px;">
                                    <div style="color: #fde68a; font-size: 0.95rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">
                                        ⚠️ Video Assessment
                                    </div>
                                    <div style="color: #ffffff; font-size: 2.5rem; font-weight: 800; margin: 8px 0;">
                                        BLURRY
                                    </div>
                                    <div style="color: #fcd34d; font-size: 1.15rem; font-weight: 600;">
                                        {final_pred.get('reason', 'Video frames are too blurry for plant identification.')}
                                    </div>
                                    <div style="color: #cbd5e1; font-size: 0.95rem; margin-top: 10px;">
                                        Analyzed: <strong>{v_result['frames_used']} frames</strong> (0 clear plant specimens found)
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                        elif final_status == "unknown":
                            st.markdown(
                                f"""
                                <div style="background-color: #1e293b; border: 2px solid #64748b; border-radius: 12px; padding: 24px; margin-bottom: 20px;">
                                    <div style="color: #cbd5e1; font-size: 0.95rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">
                                        🔍 Video Assessment
                                    </div>
                                    <div style="color: #ffffff; font-size: 2.5rem; font-weight: 800; margin: 8px 0;">
                                        UNKNOWN
                                    </div>
                                    <div style="color: #94a3b8; font-size: 1.15rem; font-weight: 600;">
                                        {final_pred.get('reason', 'No proper plant, flower, or leaf detected in video.')}
                                    </div>
                                    <div style="color: #64748b; font-size: 0.95rem; margin-top: 10px;">
                                        Analyzed: <strong>{v_result['frames_used']} frames</strong> ({v_result.get('valid_plant_frames', 0)} identifiable plant frames)
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                        else:
                            st.markdown(
                                f"""
                                <div style="background-color: #064e3b; border: 2px solid #10b981; border-radius: 12px; padding: 24px; margin-bottom: 20px;">
                                    <div style="color: #6ee7b7; font-size: 0.95rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">
                                        Plant / Crop Identification
                                    </div>
                                    <div style="color: #ffffff; font-size: 2.5rem; font-weight: 800; margin: 8px 0;">
                                        {final_pred['label'].upper()}
                                    </div>
                                    <div style="color: #a7f3d0; font-size: 1.3rem; font-weight: 600;">
                                        Aggregated Probability: <span style="color:#ffffff;">{final_pred['percentage']}</span>
                                    </div>
                                    <div style="color: #cbd5e1; font-size: 0.95rem; margin-top: 10px;">
                                        Identified across <strong>{v_result.get('valid_plant_frames', v_result['frames_used'])} clear plant frames</strong>
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                    with res_col2:
                        if final_status == "valid":
                            st.markdown("##### 📈 Top-3 Final Predictions")
                            for item in v_result["top_k"]:
                                c_lbl, c_val = st.columns([3, 1])
                                with c_lbl:
                                    st.write(f"**{item['rank']}. {item['label']}**")
                                with c_val:
                                    st.write(f"`{item['percentage']}`")
                                st.progress(item["confidence"])
                        else:
                            st.markdown("##### ℹ️ Detection Summary")
                            st.info(
                                f"**Result: {final_pred['label']}**\n\n"
                                f"{final_pred.get('reason', 'No recognizable plant/crop specimen found.')}\n\n"
                                "The system did not force a crop prediction because the video frames did not satisfy "
                                "sharpness or plant presence requirements."
                            )

                    # Frame Sampling Metrics
                    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
                    with m_col1:
                        st.metric("Total Frames Sampled", v_result["frames_used"])
                    with m_col2:
                        st.metric("Identified Plant Frames", f"{v_result.get('valid_plant_frames', 0)} / {v_result['frames_used']}")
                    with m_col3:
                        st.metric("Candidate Frames Evaluated", v_result["total_evaluated"])
                    with m_col4:
                        v_meta = v_result["video"]
                        st.metric("Video Duration", f"{v_meta['duration_seconds']:.1f}s ({v_meta['fps']:.1f} FPS)")

                    # Status alert if video had fewer usable frames than target
                    if v_result.get("status_note"):
                        st.info(f"ℹ️ {v_result['status_note']}")

                    # ----------------------------------------------------
                    # SECTION: EXTRACTED FRAME REVIEW (SHOWING ALL FRAMES)
                    # ----------------------------------------------------
                    st.markdown("---")
                    st.markdown("### 🖼 EXTRACTED FRAME REVIEW")
                    st.markdown(
                        f"**Showing all {v_result['frames_used']} frames used for inference** "
                        f"(sampled uniformly across video from 0.00s to {v_meta['duration_seconds']:.2f}s):"
                    )

                    # 4-column responsive grid displaying EVERY processed frame
                    frames_list = v_result["frame_records"]
                    cols_per_row = 4

                    for row_start in range(0, len(frames_list), cols_per_row):
                        row_frames = frames_list[row_start : row_start + cols_per_row]
                        cols = st.columns(cols_per_row)

                        for col, f in zip(cols, row_frames):
                            with col:
                                st.image(f["thumbnail"], use_container_width=True)
                                f_st = f.get("status", "valid")
                                if f_st == "blurry":
                                    badge_html = '<span style="background: #78350f; color: #fde68a; padding: 2px 8px; border-radius: 4px; font-size: 0.72rem; font-weight: 700;">⚠️ BLURRY</span>'
                                    title_html = '<div style="font-size: 1.05rem; font-weight: 700; color: #fbbf24; margin-top: 4px;">Blurry</div>'
                                    sub_html = f'<div style="font-size: 0.8rem; color: #fcd34d; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="{f.get("reason", "")}">{f.get("reason", "Low sharpness")}</div>'
                                    card_border = "#f59e0b"
                                elif f_st == "unknown":
                                    badge_html = '<span style="background: #334155; color: #cbd5e1; padding: 2px 8px; border-radius: 4px; font-size: 0.72rem; font-weight: 700;">🔍 UNKNOWN</span>'
                                    title_html = '<div style="font-size: 1.05rem; font-weight: 700; color: #cbd5e1; margin-top: 4px;">Unknown</div>'
                                    sub_html = f'<div style="font-size: 0.8rem; color: #94a3b8; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="{f.get("reason", "")}">{f.get("reason", "No plant visible")}</div>'
                                    card_border = "#64748b"
                                else:
                                    badge_html = '<span style="background: #064e3b; color: #6ee7b7; padding: 2px 8px; border-radius: 4px; font-size: 0.72rem; font-weight: 700;">🌿 PLANT SPECIMEN</span>'
                                    title_html = f'<div style="font-size: 1.05rem; font-weight: 700; color: #f8fafc; margin-top: 4px;">{f["predicted_label"]}</div>'
                                    sub_html = f'<div style="font-size: 0.85rem; color: #34d399; font-weight: 600;">Confidence: {f["percentage"]}</div>'
                                    card_border = "#10b981"

                                st.markdown(
                                    f"""
                                    <div style="background-color: #1e293b; border-radius: 8px; padding: 10px 12px; margin-bottom: 16px; border: 1.5px solid {card_border};">
                                        <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.82rem; color: #94a3b8;">
                                            <span><strong>Frame {f['frame_number']}</strong> ({f['timestamp_seconds']:.2f}s)</span>
                                            {badge_html}
                                        </div>
                                        {title_html}
                                        {sub_html}
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )

                    # ----------------------------------------------------
                    # SECTION: FRAME-LEVEL RESULTS TABLE
                    # ----------------------------------------------------
                    st.markdown("##### 📋 Detailed Frame-by-Frame Results")
                    table_rows = []
                    for f in frames_list:
                        top2_info = f["top_k"][1]["label"] if len(f.get("top_k", [])) > 1 else "-"
                        f_st = f.get("status", "valid")
                        status_str = "Valid Plant" if f_st == "valid" else ("Blurry" if f_st == "blurry" else "Unknown (No Plant)")
                        table_rows.append({
                            "Frame #": f["frame_number"],
                            "Source Frame Index": f["frame_index"],
                            "Timestamp": f"{f['timestamp_seconds']:.2f}s",
                            "Visual Status": status_str,
                            "Prediction": f["predicted_label"],
                            "Confidence": f["percentage"],
                            "Reason / Assessment": f.get("reason", "-"),
                            "Runner-Up (Top 2)": top2_info,
                            "Quality Score": f"{f['quality_score']:.2f}",
                        })

                    st.dataframe(table_rows, use_container_width=True, hide_index=True)

                except InvalidVideoError as exc:
                    st.error(f"Invalid Video Error: {exc}")
                except EmptyVideoError as exc:
                    st.error(f"Empty Video Error: {exc}")
                except Exception as exc:
                    st.error(f"Video classification failure: {exc}")
                finally:
                    if tmp_video_path.exists():
                        try:
                            tmp_video_path.unlink()
                        except OSError:
                            pass

    # Reference class inventory expander
    with st.expander("📚 Model 1 Supported Plant / Crop Classes (22 Classes)"):
        cols = st.columns(4)
        sorted_classes = sorted(idx_to_class.values())
        for idx, cls_name in enumerate(sorted_classes):
            with cols[idx % 4]:
                st.markdown(f"&bull; **{cls_name.replace('_', ' ').title()}** (`{cls_name}`)")


if __name__ == "__main__":
    main()
