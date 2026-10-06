import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(36, 762, "Fashion-MNIST ANN Pipeline | Git, DVC & Google Drive Versioning Report")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(36, 756, 576, 756)
            
        # Footer
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(36, 36, 576, 36)
        
        repo_text = "GitHub Repository: https://github.com/Android1289/fashion-ann-pipeline"
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawString(36, 25, repo_text)
        self.drawRightString(576, 25, page_text)
        self.restoreState()

def build_pdf(filename="Fashion_ANN_Pipeline_Report.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=38,
        bottomMargin=38
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=2
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#475569'),
        spaceAfter=6
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#1E3A8A'),
        spaceBefore=5,
        spaceAfter=3,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=4,
        spaceAfter=2,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor('#334155'),
        spaceAfter=3
    )

    code_style = ParagraphStyle(
        'CodeSnippet',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=6.8,
        leading=8.5,
        textColor=colors.HexColor('#0F172A'),
        backColor=colors.HexColor('#F1F5F9'),
        borderColor=colors.HexColor('#CBD5E1'),
        borderWidth=0.5,
        borderPadding=3,
        spaceBefore=2,
        spaceAfter=3
    )

    meta_table_style = ParagraphStyle(
        'MetaTableText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=9.8,
        textColor=colors.HexColor('#1E293B')
    )

    meta_table_bold = ParagraphStyle(
        'MetaTableBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.8,
        leading=9.8,
        textColor=colors.HexColor('#0F172A')
    )

    elements = []

    # Title & Header
    elements.append(Paragraph("End-to-End ML Versioning with Git, DVC & Google Drive", title_style))
    elements.append(Paragraph("Comprehensive Technical Report | Fashion-MNIST ANN Pipeline Reproduction & Conflict Resolution", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=1.2, color=colors.HexColor('#1E3A8A'), spaceBefore=1, spaceAfter=5))

    # Metadata Card Table
    meta_data = [
        [Paragraph("<b>Student Author:</b>", meta_table_bold), Paragraph("Android AP (abubakaramir128@gmail.com)", meta_table_style),
         Paragraph("<b>Target Metric:</b>", meta_table_bold), Paragraph("Test Accuracy ≥ 85% (Achieved: 87.72%)", meta_table_style)],
        [Paragraph("<b>GitHub Repo:</b>", meta_table_bold), Paragraph("<font color='#1E40AF'><u>https://github.com/Android1289/fashion-ann-pipeline</u></font>", meta_table_style),
         Paragraph("<b>DVC Remote:</b>", meta_table_bold), Paragraph("Google Drive (<code>gdrive://1nezVkmPAtYrslDtxP-jrDtsCU-eYjaTf</code>)", meta_table_style)],
        [Paragraph("<b>Frameworks:</b>", meta_table_bold), Paragraph("TensorFlow 2.21, DVC 3.67, PyDrive2, Git 2.47", meta_table_style),
         Paragraph("<b>Dataset:</b>", meta_table_bold), Paragraph("Fashion-MNIST (70,000 28x28 grayscale images, 10 classes)", meta_table_style)]
    ]
    meta_table = Table(meta_data, colWidths=[85, 195, 75, 185])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    elements.append(meta_table)
    elements.append(Spacer(1, 4))

    # SECTION A: GIT ADVANCED COMMANDS
    elements.append(Paragraph("Part A — Git Fundamentals & Advanced Commands", h1_style))
    elements.append(Paragraph(
        "<b>A1 & A2 (Repository Setup & Incremental Commits):</b> The project was initialized on branch <code>main</code> with an initial commit containing <code>README.md</code> and <code>.gitignore</code> (configured to exclude Python caches, virtual environments, credentials, and DVC payload folders). Feature branch <code>dev</code> was created (<code>git checkout -b dev</code>) where all pipeline work was developed using 7 incremental, atomic commits representing each script and configuration component.",
        body_style
    ))
    
    # A3: Log Variants
    elements.append(Paragraph("A3 — Git Log Variants & Explanations", h2_style))
    a3_text = (
        "<b>1. <code>git log --oneline --graph --all</code>:</b> Displays the entire commit DAG across all branches in compact single-line format with ASCII branch visualizers, revealing branch topology and merge divergences.<br/>"
        "<b>2. <code>git log --stat -3</code>:</b> Appends diffstat summaries to the last 3 commits, revealing which files were modified and the exact line insertion/deletion count per commit.<br/>"
        "<b>3. <code>git log -p -1</code>:</b> Shows the full line-by-line unified patch for the most recent commit, revealing exact content modifications.<br/>"
        "<b>4. <code>git log main..dev</code>:</b> Performs symmetric difference filtering, displaying exclusively commits reachable from <code>dev</code> that are not in <code>main</code>."
    )
    elements.append(Paragraph(a3_text, body_style))
    
    a3_terminal = (
        "$ git log --oneline --graph --all\n"
        "* 7536b8a (HEAD -> main) Merge branch 'teammate-sim': Reconcile normalization strategies and DVC data pointers\n"
        "|\\  \n"
        "| * 44cdc83 (teammate-sim) teammate-sim: update normalization to z-score standardization\n"
        "* | 6092274 main: update normalization to [-1, 1] range\n"
        "|/  \n"
        "| * a6a07de (tag: v2, dev) Update hyperparameters (dense_units=512) and record v2 metrics\n"
        "|/  \n"
        "* 0488933 (tag: v1) Track DVC pipeline execution v1 artifacts and metrics\n"
        "* ff0360c Remove temporary utility script\n"
        "* d6453fe Cleanup: Remove obsolete scratch notes using git rm\n"
        "* 1a11c31 Reorganize: Move helper utility into src/ package using git mv\n"
        "* 3225789 Add auxiliary utility and notes\n"
        "* 80c317d Author DVC pipeline stages for end-to-end reproducibility (dvc.yaml)\n"
        "* 0785fc5 Add central hyperparameters configuration (params.yaml)\n"
        "* 4d37df1 Add model evaluation, confusion matrix, and metrics script (src/evaluate.py)\n"
        "* ee1166c Add TensorFlow ANN model training script (src/train.py)\n"
        "* 2456aa7 Add data preprocessing and validation split script (src/preprocess.py)\n"
        "* fe5374f Add data preparation stage script (src/prepare.py)\n"
        "* bc33b9b Initialize DVC with Google Drive remote storage\n"
        "*   35561a2 Merge hotfix branch into main\n"
        "|\\  \n"
        "| * 2dce22f hotfix: Improve README description and formatting\n"
        "|/  \n"
        "* 4e152ad Initial project setup"
    )
    elements.append(Paragraph(a3_terminal.replace('\n', '<br/>').replace(' ', '&nbsp;'), code_style))

    # A4: Diff Variants
    elements.append(Paragraph("A4 — Diff Variants & Branch Comparison", h2_style))
    elements.append(Paragraph(
        "• <b><code>git diff</code>:</b> Compares unstaged modifications in working tree against index.<br/>"
        "• <b><code>git diff --staged</code>:</b> Compares indexed (staged) changes against <code>HEAD</code>.<br/>"
        "• <b>Two-Dot (<code>main..dev</code>) vs Three-Dot (<code>main...dev</code>):</b><br/>"
        "&nbsp;&nbsp;- <code>git diff main..dev</code> compares current tips of both branches directly.<br/>"
        "&nbsp;&nbsp;- <code>git diff main...dev</code> computes diff between common merge base ancestor of <code>main</code> and <code>dev</code> up to <code>dev</code>, isolating only changes introduced on <code>dev</code>.",
        body_style
    ))

    # A5, A6, A7, A8
    elements.append(Paragraph("A5 to A8 — Advanced Git Scenarios (Stash, Rebase, Reset, Mv & Rm)", h2_style))
    elements.append(Paragraph(
        "• <b>A5 (Stash Scenario):</b> While mid-edit on <code>src/preprocess.py</code>, changes were stashed via <code>git stash push -m 'WIP: Preprocessing verification edit'</code>, allowing clean context-switching to <code>main</code> and back to <code>dev</code>. <code>git stash list</code> verified stash persistence before restoring via <code>git stash pop</code>.<br/>"
        "• <b>A6 (Rebase Scenario):</b> A critical <code>hotfix</code> branch was branched from <code>main</code>, committed, and merged into <code>main</code> (commit <code>35561a2</code>). From <code>dev</code>, <code>git rebase main</code> was executed, replaying all 7 feature commits cleanly on top of <code>main</code> without merge bubbles.<br/>"
        "• <b>A7 (Reset Scenario):</b> On a temporary <code>scratch</code> branch: <code>git reset --soft HEAD~1</code> undid the commit while keeping modified files staged in the index (verified by <code>git status</code>). Next, <code>git reset --hard HEAD~1</code> completely discarded both commit and working tree modifications, leaving repository clean.<br/>"
        "• <b>A8 (Reorganize with git mv & git rm):</b> Loose utility scripts were reorganized into <code>src/</code> via <code>git mv temp_helper.py src/utils.py</code> and committed as tracked rename events (100% rename similarity). Obsolete scratch notes were pruned via <code>git rm notes_scratch.md</code> as tracked deletion events.",
        body_style
    ))
    elements.append(Spacer(1, 4))

    # SECTION B: MODULAR TF ANN PIPELINE
    elements.append(Paragraph("Part B — Modular TensorFlow ANN Pipeline Architecture", h1_style))
    elements.append(Paragraph(
        "The project decomposes the Machine Learning workflow into four single-responsibility, independent Python scripts inside <code>src/</code>:",
        body_style
    ))
    
    pipeline_stages_data = [
        [Paragraph("<b>Script</b>", meta_table_bold), Paragraph("<b>Input Dependencies</b>", meta_table_bold), Paragraph("<b>Produced Outputs</b>", meta_table_bold), Paragraph("<b>Role & Methodology</b>", meta_table_bold)],
        [Paragraph("<code>src/prepare.py</code>", meta_table_style), Paragraph("Fashion-MNIST remote source", meta_table_style), Paragraph("<code>data/raw/*.npy, *.gz</code>", meta_table_style), Paragraph("Downloads and extracts raw ubyte archives; saves 60,000 train and 10,000 test image/label arrays.", meta_table_style)],
        [Paragraph("<code>src/preprocess.py</code>", meta_table_style), Paragraph("<code>data/raw/</code>, <code>params.yaml</code>", meta_table_style), Paragraph("<code>data/processed/*.npy</code>", meta_table_style), Paragraph("Normalizes pixels to [0, 1] float32; performs stratified 80/20 train-validation split (48k train, 12k val).", meta_table_style)],
        [Paragraph("<code>src/train.py</code>", meta_table_style), Paragraph("<code>data/processed/</code>, <code>params.yaml</code>", meta_table_style), Paragraph("<code>models/model.h5</code>, <code>history.csv</code>", meta_table_style), Paragraph("Constructs Sequential ANN: Flatten(28,28) → Dense(ReLU) → Dropout → Dense(10, Softmax). Trains with Adam & Sparse Categorical Crossentropy.", meta_table_style)],
        [Paragraph("<code>src/evaluate.py</code>", meta_table_style), Paragraph("<code>models/model.h5</code>, <code>data/processed/</code>", meta_table_style), Paragraph("<code>metrics.json</code>, <code>confusion_matrix.png</code>", meta_table_style), Paragraph("Evaluates on test partition (10,000 images). Computes loss, accuracy, generates ConfusionMatrixDisplay.", meta_table_style)]
    ]
    p_table = Table(pipeline_stages_data, colWidths=[85, 110, 115, 230])
    p_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#94A3B8')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 3.5),
        ('RIGHTPADDING', (0,0), (-1,-1), 3.5),
    ]))
    elements.append(p_table)
    elements.append(Spacer(1, 4))

    # SECTION C: DVC SETUP WITH GDRIVE
    elements.append(Paragraph("Part C — DVC Setup with Google Drive Remote Storage", h1_style))
    elements.append(Paragraph(
        "<b>Remote Storage Architecture:</b> DVC was initialized on feature branch <code>dev</code> (<code>dvc init</code>) and configured with Google Drive remote storage pointing to folder ID <code>1nezVkmPAtYrslDtxP-jrDtsCU-eYjaTf</code>:<br/>"
        "<code>dvc remote add -d gdrive_storage gdrive://1nezVkmPAtYrslDtxP-jrDtsCU-eYjaTf</code><br/>"
        "<b>Security & Payload Isolation:</b> <code>.gitignore</code> strictly excludes heavy dataset payloads (<code>data/raw/</code>, <code>data/processed/</code>), model binaries (<code>models/</code>), plot outputs (<code>confusion_matrix.png</code>), and Google OAuth client tokens (<code>credentials.json</code>, <code>*.token</code>). Git exclusively versions lightweight hash pointer files (<code>dvc.lock</code>) while DVC manages remote payload synchronization.",
        body_style
    ))
    elements.append(Spacer(1, 4))

    # SECTION D: DVC PIPELINE & HYPERPARAMETER TUNING
    elements.append(Paragraph("Part D — DVC Pipeline Execution & Hyperparameter Tuning (D3 vs D4)", h1_style))
    elements.append(Paragraph(
        "<b>DVC Pipeline Authoring:</b> The four stages were wired into <code>dvc.yaml</code> with precise granular dependencies and parameters. Hyperparameters are centralized in <code>params.yaml</code>.",
        body_style
    ))

    # D3 vs D4 Logs
    d_log_text = (
        "--- D3 EXECUTION (Initial Run - All Stages Execute) ---\n"
        "$ dvc repro\n"
        "Running stage 'prepare': > python src/prepare.py [Downloaded and saved 8 raw files]\n"
        "Running stage 'preprocess': > python src/preprocess.py [Processed 60k train/val, 10k test]\n"
        "Running stage 'train': > python src/train.py [Epochs: 10, dense_units: 256, val_acc: 89.20%]\n"
        "Running stage 'evaluate': > python src/evaluate.py [Test Loss: 0.3408, Test Acc: 87.72%]\n"
        "Updating lock file 'dvc.lock'\n\n"
        "--- D4 EXECUTION (Hyperparameter Tuning: dense_units increased from 256 to 512) ---\n"
        "$ dvc repro\n"
        "Stage 'prepare' didn't change, skipping\n"
        "Stage 'preprocess' didn't change, skipping\n"
        "Running stage 'train': > python src/train.py [Epochs: 10, dense_units: 512, val_acc: 88.44%]\n"
        "Running stage 'evaluate': > python src/evaluate.py [Test Loss: 0.3587, Test Acc: 87.37%]\n"
        "Updating lock file 'dvc.lock'"
    )
    elements.append(Paragraph(d_log_text.replace('\n', '<br/>').replace(' ', '&nbsp;'), code_style))

    elements.append(Paragraph(
        "<b>Technical Explanation of Skipped Stages (D4):</b> In D4, DVC checked md5 hashes of stage dependencies. Stages <code>prepare</code> and <code>preprocess</code> depend on <code>src/prepare.py</code>, <code>src/preprocess.py</code>, <code>data/raw</code>, and <code>params.yaml:preprocess</code> — none of which changed. Therefore, DVC skipped them, saving significant computation. In contrast, <code>train</code> depends on <code>params.yaml:train.dense_units</code> which changed from 256 to 512, invalidating the stage lock. Since <code>train</code> produced a new <code>models/model.h5</code>, stage <code>evaluate</code> also automatically re-executed.",
        body_style
    ))
    elements.append(Spacer(1, 3))

    # V1 vs V2 Metrics Comparison Table
    elements.append(Paragraph("Hyperparameter & Performance Comparison: Version 1 (v1) vs Version 2 (v2)", h2_style))
    metrics_data = [
        [Paragraph("<b>Experiment Version</b>", meta_table_bold), Paragraph("<b>Dense Units</b>", meta_table_bold), Paragraph("<b>Dropout Rate</b>", meta_table_bold), Paragraph("<b>Learning Rate</b>", meta_table_bold), Paragraph("<b>Validation Acc</b>", meta_table_bold), Paragraph("<b>Test Accuracy</b>", meta_table_bold), Paragraph("<b>Test Loss</b>", meta_table_bold)],
        [Paragraph("<b>Version 1 (v1)</b>", meta_table_style), Paragraph("256", meta_table_style), Paragraph("0.2", meta_table_style), Paragraph("0.001", meta_table_style), Paragraph("89.20%", meta_table_style), Paragraph("<b>87.72%</b>", meta_table_bold), Paragraph("0.3408", meta_table_style)],
        [Paragraph("<b>Version 2 (v2)</b>", meta_table_style), Paragraph("512", meta_table_style), Paragraph("0.2", meta_table_style), Paragraph("0.001", meta_table_style), Paragraph("88.44%", meta_table_style), Paragraph("<b>87.37%</b>", meta_table_bold), Paragraph("0.3587", meta_table_style)]
    ]
    m_table = Table(metrics_data, colWidths=[95, 70, 70, 75, 75, 75, 80])
    m_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#F8FAFC')),
        ('BACKGROUND', (0,2), (-1,2), colors.HexColor('#FFFFFF')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#94A3B8')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ALIGN', (1,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    elements.append(m_table)
    elements.append(Spacer(1, 4))

    # SECTION E: SIMULATED COLLABORATION & CONFLICT RESOLUTION
    elements.append(Paragraph("Part E — Simulated Collaboration & Simultaneous Dual Conflict Resolution", h1_style))
    elements.append(Paragraph(
        "To simulate realistic team collaboration, two divergent branches were created from <code>v1</code> on <code>main</code>, both introducing conflicting normalization algorithms and regenerating divergent preprocessed data arrays.",
        body_style
    ))
    
    conflict_desc = (
        "• <b>Branch <code>teammate-sim</code> (E1):</b> Implemented <b>Z-score standardization</b> (<code>(x - mean) / std</code>). Re-ran <code>dvc repro preprocess</code>, generating processed data with hash <code>d7169048...dir</code>.<br/>"
        "• <b>Branch <code>main</code> (E2):</b> Independently implemented <b>Min-Max scaling to [-1, 1]</b> (<code>(x / 127.5) - 1.0</code>). Re-ran <code>dvc repro preprocess</code>, generating processed data with hash <code>092a23a2...dir</code>.<br/>"
        "• <b>Merge Attempt (E3):</b> Running <code>git merge teammate-sim</code> produced simultaneous Git code and DVC pointer conflicts:"
    )
    elements.append(Paragraph(conflict_desc, body_style))

    # Conflict Log Snippet
    conflict_snippet = (
        "$ git merge teammate-sim\n"
        "Auto-merging dvc.lock\n"
        "CONFLICT (content): Merge conflict in dvc.lock\n"
        "Auto-merging src/preprocess.py\n"
        "CONFLICT (content): Merge conflict in src/preprocess.py\n"
        "Automatic merge failed; fix conflicts and then commit the result."
    )
    elements.append(Paragraph(conflict_snippet.replace('\n', '<br/>').replace(' ', '&nbsp;'), code_style))

    elements.append(Paragraph("Simultaneous Conflict Manifestation Across Code and Data Pointers", h2_style))
    diff_snippet = (
        "--- [CODE CONFLICT: src/preprocess.py] ---\n"
        "<<<<<<< HEAD\n"
        "    # Main branch normalization: Min-Max scaling to [-1, 1] range\n"
        "    x_train = (x_train.astype(\"float32\") / 127.5) - 1.0\n"
        "=======\n"
        "    # Teammate-sim normalization: Z-score standardization\n"
        "    mean = np.mean(x_train, axis=(0, 1, 2), keepdims=True)\n"
        "    x_train = (x_train.astype(\"float32\") - mean) / std\n"
        ">>>>>>> teammate-sim\n\n"
        "--- [DVC POINTER CONFLICT: dvc.lock (stage preprocess)] ---\n"
        "    outs:\n"
        "    - path: data/processed\n"
        "<<<<<<< HEAD\n"
        "      md5: 092a23a2c39b574669a7a655fadc4d85.dir\n"
        "=======\n"
        "      md5: d716904822b580ae72326cd16e98f50b.dir\n"
        ">>>>>>> teammate-sim"
    )
    elements.append(Paragraph(diff_snippet.replace('\n', '<br/>').replace(' ', '&nbsp;'), code_style))

    # E4 and E5 Resolution
    elements.append(Paragraph("Resolution Strategy & Verification (E4 & E5):", h2_style))
    elements.append(Paragraph(
        "<b>1. Code Reconciliation:</b> In <code>src/preprocess.py</code>, both approaches were reconciled by selecting standard [0, 1] float32 feature normalization, optimal for sigmoid/softmax outputs and neural gradient stability.<br/>"
        "<b>2. Data Hash Reconciliation:</b> The conflict markers in <code>dvc.lock</code> were removed. <code>dvc repro preprocess</code> was executed to deterministically regenerate authoritative data payloads matching reconciled code, computing valid md5 <code>eeb8cf24...dir</code>.<br/>"
        "<b>3. Workspace Synchronization:</b> <code>dvc checkout</code> synchronized local payload caches with the active pointer.<br/>"
        "<b>4. Verification:</b> <code>dvc status</code> verified <code>'Data and pipelines are up to date'</code>. The merge commit was sealed (commit <code>7536b8a</code>) and <code>dvc repro</code> confirmed end-to-end reproducibility.",
        body_style
    ))
    elements.append(Spacer(1, 4))

    # SECTION F: VERIFICATION & SUMMARY CHECKLIST
    elements.append(Paragraph("Deliverables Verification Checklist", h1_style))
    check_data = [
        [Paragraph("<b>Item / Deliverable</b>", meta_table_bold), Paragraph("<b>Requirement</b>", meta_table_bold), Paragraph("<b>Status</b>", meta_table_bold), Paragraph("<b>Reference Details</b>", meta_table_bold)],
        [Paragraph("<b>GitHub Repository</b>", meta_table_style), Paragraph("Unsquashed commit history (Parts A–E)", meta_table_style), Paragraph("<font color='#16A34A'><b>VERIFIED</b></font>", meta_table_style), Paragraph("Branches: <code>main</code>, <code>dev</code>, <code>teammate-sim</code>; Tags: <code>v1</code>, <code>v2</code>", meta_table_style)],
        [Paragraph("<b>ANN Accuracy</b>", meta_table_style), Paragraph("Test Accuracy ≥ 85% on Fashion-MNIST", meta_table_style), Paragraph("<font color='#16A34A'><b>VERIFIED</b></font>", meta_table_style), Paragraph("v1: <b>87.72%</b>, v2: <b>87.37%</b> (both exceed rubric threshold)", meta_table_style)],
        [Paragraph("<b>DVC Remote Storage</b>", meta_table_style), Paragraph("Google Drive storage registration", meta_table_style), Paragraph("<font color='#16A34A'><b>VERIFIED</b></font>", meta_table_style), Paragraph("Folder ID: <code>1nezVkmPAtYrslDtxP-jrDtsCU-eYjaTf</code>", meta_table_style)],
        [Paragraph("<b>DVC Pipeline</b>", meta_table_style), Paragraph("<code>dvc.yaml</code>, <code>params.yaml</code>, <code>dvc repro</code>", meta_table_style), Paragraph("<font color='#16A34A'><b>VERIFIED</b></font>", meta_table_style), Paragraph("4 stages (prepare, preprocess, train, evaluate); lock generated", meta_table_style)],
        [Paragraph("<b>Git Advanced Operations</b>", meta_table_style), Paragraph("Log, diff, stash, rebase, reset, mv, rm", meta_table_style), Paragraph("<font color='#16A34A'><b>VERIFIED</b></font>", meta_table_style), Paragraph("All workflows demonstrated and verified in commit tree", meta_table_style)],
        [Paragraph("<b>Dual Conflict Resolution</b>", meta_table_style), Paragraph("Code & pointer conflict resolution", meta_table_style), Paragraph("<font color='#16A34A'><b>VERIFIED</b></font>", meta_table_style), Paragraph("Reconciled merge commit <code>7536b8a</code> cleanly committed", meta_table_style)]
    ]
    c_table = Table(check_data, colWidths=[105, 145, 60, 230])
    c_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#94A3B8')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ALIGN', (2,1), (2,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 3.5),
        ('RIGHTPADDING', (0,0), (-1,-1), 3.5),
    ]))
    elements.append(c_table)

    doc.build(elements, canvasmaker=NumberedCanvas)
    print(f"Report successfully generated at: {filename}")

if __name__ == "__main__":
    build_pdf("Fashion_ANN_Pipeline_Report.pdf")
