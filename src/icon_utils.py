"""Utility functions for handling icons and images."""

import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path
from typing import Optional, Tuple
import customtkinter as ctk
from .constants import GAME_ICON


class IconManager:
    """Manages application icons and images."""

    def __init__(self):
        self._cached_icons = {}

    def _resize_with_aspect_ratio(self, image: Image.Image, target_size: Tuple[int, int]) -> Image.Image:
        """
        Resize image while maintaining aspect ratio.

        Args:
            image: PIL Image to resize
            target_size: (width, height) target size

        Returns:
            Resized PIL Image
        """
        original_width, original_height = image.size
        target_width, target_height = target_size

        # Calculate aspect ratios
        original_ratio = original_width / original_height
        target_ratio = target_width / target_height

        if original_ratio > target_ratio:
            # Image is wider than target - fit to width
            new_width = target_width
            new_height = int(target_width / original_ratio)
        else:
            # Image is taller than target - fit to height
            new_height = target_height
            new_width = int(target_height * original_ratio)

        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    def set_window_icon(self, window: tk.Tk) -> bool:
        """
        Set the window icon for the application.

        Args:
            window: The tkinter window to set the icon for

        Returns:
            bool: True if icon was set successfully, False otherwise
        """
        try:
            if GAME_ICON.exists():
                # For Windows .ico files
                if GAME_ICON.suffix.lower() == '.ico':
                    window.iconbitmap(str(GAME_ICON))
                    return True

                # For PNG/other image files, convert to PhotoImage
                image = Image.open(GAME_ICON)

                # Resize if too large (Windows taskbar icons are typically 32x32 or 16x16)
                # But maintain aspect ratio
                if image.size[0] > 64 or image.size[1] > 64:
                    image = self._resize_with_aspect_ratio(image, (32, 32))

                photo = ImageTk.PhotoImage(image)
                window.iconphoto(True, photo)

                # Keep a reference to prevent garbage collection
                window._icon_reference = photo
                return True
            else:
                print(f"Icon file not found: {GAME_ICON}")
                return False

        except Exception as e:
            print(f"Failed to set window icon: {e}")
            return False

    def get_resized_icon(self, size: Tuple[int, int], maintain_aspect: bool = True) -> Optional[ImageTk.PhotoImage]:
        """
        Get a resized version of the game icon.

        Args:
            size: Tuple of (width, height) for the desired size
            maintain_aspect: Whether to maintain aspect ratio

        Returns:
            PhotoImage object or None if failed
        """
        try:
            cache_key = f"{size[0]}x{size[1]}_aspect_{maintain_aspect}"

            if cache_key in self._cached_icons:
                return self._cached_icons[cache_key]

            if GAME_ICON.exists():
                image = Image.open(GAME_ICON)

                if maintain_aspect:
                    image = self._resize_with_aspect_ratio(image, size)
                else:
                    image = image.resize(size, Image.Resampling.LANCZOS)

                photo = ImageTk.PhotoImage(image)

                # Cache the resized icon
                self._cached_icons[cache_key] = photo
                return photo

            return None

        except Exception as e:
            print(f"Failed to create resized icon: {e}")
            return None

    def create_ctk_image(self, size: Tuple[int, int], maintain_aspect: bool = True) -> Optional[ctk.CTkImage]:
        """
        Create a CustomTkinter CTkImage from the game icon.

        Args:
            size: Tuple of (width, height) for the desired size
            maintain_aspect: Whether to maintain aspect ratio

        Returns:
            CTkImage object or None if failed
        """
        try:
            if GAME_ICON.exists():
                image = Image.open(GAME_ICON)

                if maintain_aspect:
                    image = self._resize_with_aspect_ratio(image, size)
                else:
                    image = image.resize(size, Image.Resampling.LANCZOS)

                # CTkImage handles light/dark mode automatically
                return ctk.CTkImage(light_image=image, dark_image=image, size=(image.width, image.height))

            return None

        except Exception as e:
            print(f"Failed to create CTkImage: {e}")
            return None

    def get_image_info(self) -> Optional[dict]:
        """
        Get information about the game icon.

        Returns:
            Dictionary with image info or None if failed
        """
        try:
            if GAME_ICON.exists():
                image = Image.open(GAME_ICON)
                return {
                    "size": image.size,
                    "format": image.format,
                    "mode": image.mode,
                    "width": image.width,
                    "height": image.height,
                    "aspect_ratio": image.width / image.height
                }
            return None
        except Exception as e:
            print(f"Failed to get image info: {e}")
            return None


# Global instance
icon_manager = IconManager()