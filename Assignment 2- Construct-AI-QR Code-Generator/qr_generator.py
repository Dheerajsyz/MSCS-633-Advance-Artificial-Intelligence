#!/usr/bin/env python3
"""Simple QR Code Generator for Biox Systems.

Provides both a Tkinter GUI and a CLI fallback for generating QR codes
from a supplied URL. The GUI is launched by default if Tkinter + PIL are
available; otherwise the program falls back to CLI mode or can be forced
with ``--cli``.
"""

from __future__ import annotations

import argparse
import os
import qrcode
from typing import Optional

try:  # GUI / image display dependencies
    import tkinter as tk
    from tkinter import filedialog
    from PIL import Image, ImageTk
    GUI_AVAILABLE = True
except Exception:  # pragma: no cover - environment without GUI libs
    GUI_AVAILABLE = False

# ------------------------------ Constants ------------------------------ #
TITLE_FONT = ("Arial", 24, "bold")
LABEL_FONT = ("Arial", 14)
ENTRY_FONT = ("Arial", 12)
BTN_FONT = ("Arial", 14, "bold")
INFO_FONT = ("Arial", 11)
TIP_FONT = ("Arial", 10)

BLUE = "#1E90FF"   # Generate button color
GREEN = "#32CD32"  # Save button color
QR_SIZE = 280


def generate_qr_code(url: str, output_path: Optional[str] = None):
    """Return a Pillow image containing a QR code for ``url``.

    If ``output_path`` is provided the image is also written to disk.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    if output_path:
        img.save(output_path)
        print(f"Saved: {output_path}")
    return img


def gui_mode() -> None:
    """Launch the Tkinter GUI (no-op if GUI isn't available)."""
    if not GUI_AVAILABLE:
        print("GUI mode not available. Use command-line mode instead.")
        return

    root = tk.Tk()
    root.title("⚡ Biox Systems QR Code Generator")
    root.geometry("550x650")
    root.configure(bg='white')
    root.resizable(False, False)

    main_frame = tk.Frame(root, padx=25, pady=25, bg='white')
    main_frame.pack(expand=True, fill='both')

    title_label = tk.Label(
        main_frame,
        text="QR Code Generator",
        font=TITLE_FONT,
        fg='black',
        bg='white',
    )
    title_label.pack(pady=(0, 25))

    url_label = tk.Label(
        main_frame,
        text="Website URL:",
        font=LABEL_FONT,
        fg='black',
        bg='white',
    )
    url_label.pack(anchor='w', pady=(0, 5))

    url_entry = tk.Entry(main_frame, font=ENTRY_FONT, width=50)
    url_entry.pack(fill='x', pady=(0, 20), ipady=8)
    url_entry.insert(0, "https://www.bioxsystems.com/")
    url_entry.select_range(0, tk.END)

    generate_btn = tk.Button(
        main_frame,
        text="🚀 Generate QR",
        font=BTN_FONT,
        bg=BLUE,
        fg='black',
        padx=20,
        pady=10,
        relief='raised',
        bd=2,
        cursor='hand2',
    )
    generate_btn.pack(fill='x', pady=(0, 10))

    save_btn = tk.Button(
        main_frame,
        text="💾 Save QR",
        font=BTN_FONT,
        bg=GREEN,
        fg='black',
        padx=20,
        pady=10,
        relief='raised',
        bd=2,
        cursor='hand2',
        state='disabled',
    )
    save_btn.pack(fill='x', pady=(0, 20))

    qr_frame = tk.Frame(main_frame, bg='white', relief='solid', bd=1)
    qr_frame.pack(pady=(0, 10), padx=20)

    qr_label = tk.Label(
        qr_frame,
        text="👆 Generate",
        font=LABEL_FONT,
        fg='gray',
        bg='white',
        width=25,
        height=12,
    )
    qr_label.pack(padx=10, pady=10)

    status_label = tk.Label(
        main_frame,
        text="Ready ✅",
        font=INFO_FONT,
        fg='green',
        bg='white',
    )
    status_label.pack()

    def set_status(text: str, color: str) -> None:
        status_label.config(text=text, fg=color)

    def generate_qr():
        url = url_entry.get().strip()
        if not url:
            set_status("❌ Enter a URL", 'red')
            return

        try:
            set_status("⚡ Generating...", 'orange')
            root.update()
            img = generate_qr_code(url)
            img = img.resize((QR_SIZE, QR_SIZE))
            tk_img = ImageTk.PhotoImage(img)
            qr_label.configure(image=tk_img, text="", width=QR_SIZE, height=QR_SIZE)
            qr_label.image = tk_img
            save_btn.configure(state='normal', bg=GREEN)
            save_btn.current_img = img
            set_status("✅ Generated", 'green')
        except Exception:
            set_status("❌ Generate failed", 'red')
    
    def save_qr():  # noqa: C901 - simple enough; kept inline for clarity
        if not hasattr(save_btn, 'current_img'):
            set_status("❌ Nothing to save", 'red')
            return
        try:
            root.lift()
            root.focus_force()
            root.update_idletasks()
            root.attributes('-topmost', True)
            root.after(250, lambda: root.attributes('-topmost', False))

            default_dir = os.path.expanduser('~/Desktop')
            if not os.path.isdir(default_dir):  # fallback
                default_dir = os.path.expanduser('~')

            set_status("🗂️ Save...", 'blue')
            root.update_idletasks()

            filename = filedialog.asksaveasfilename(
                parent=root,
                title="Save QR",
                initialdir=default_dir,
                defaultextension='.png',
                initialfile='bioxsystems_qr.png',
                filetypes=[('PNG files', '*.png'), ('All files', '*.*')],
            )
            if not filename:
                set_status("❌ Cancelled", 'orange')
                return
            if not filename.lower().endswith('.png'):
                filename += '.png'
            save_btn.current_img.save(filename)
            set_status("💾 Saved", 'green')
            print(f"Saved: {filename}")
        except Exception as err:  # pragma: no cover - GUI path
            print(f"Save error: {err}")
            set_status("❌ Save failed", 'red')
    
    generate_btn.configure(command=generate_qr)
    save_btn.configure(command=save_qr)
    url_entry.focus()
    url_entry.bind('<Return>', lambda e: generate_qr())

    instructions = tk.Label(
        main_frame,
        text="💡 Tip: Press Enter after typing URL",
        font=TIP_FONT,
        fg='gray',
        bg='white',
    )
    instructions.pack(pady=(10, 0))
    root.mainloop()


def cli_mode(url: Optional[str], output: Optional[str]) -> None:
    """Simplified CLI fallback when GUI isn't used."""
    if not url:
        url = input("Enter URL: ").strip()
    if not url:
        print("Error: No URL provided")
        return
    if not output:
        safe = url.replace('://', '_').replace('/', '_')
        output = f"qr_{safe}.png"
    try:
        generate_qr_code(url, output)
        print("Generated")
    except Exception as err:
        print(f"Error: {err}")


def main() -> None:
    """Parse arguments and dispatch to GUI or CLI."""
    parser = argparse.ArgumentParser(description="QR Code Generator for Biox Systems")
    parser.add_argument('--url', '-u', help='URL to encode')
    parser.add_argument('--output', '-o', help='Output file path')
    parser.add_argument('--cli', action='store_true', help='Force CLI mode')
    args = parser.parse_args()
    if args.cli or not GUI_AVAILABLE:
        cli_mode(args.url, args.output)
    else:
        gui_mode()


if __name__ == "__main__":
    main()
