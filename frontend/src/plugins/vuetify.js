import "@mdi/font/css/materialdesignicons.css";
import "vuetify/styles";
import { createVuetify } from "vuetify";

const timeappTheme = {
  dark: false,
  colors: {
    background: "#F9FAFB", // Soft off-white
    surface: "#FFFFFF", // Pure white
    primary: "#4F46E5", // Electric Indigo
    secondary: "#0D9488", // Bright Teal
    error: "#E11D48", // Bright Rose
    info: "#3B82F6", // Blue
    success: "#10B981", // Emerald
    warning: "#F59E0B", // Amber
  },
};

export default createVuetify({
  theme: {
    defaultTheme: "timeappTheme",
    themes: {
      timeappTheme,
    },
  },
  defaults: {
    global: {
      elevation: 0,
    },
    VCard: {
      border: true,
      rounded: "xl",
    },
    VBtn: {
      rounded: "lg",
      style: "text-transform: none; letter-spacing: normal;",
      elevation: 0,
    },
    VTextField: {
      variant: "outlined",
      density: "comfortable",
      color: "primary",
    },
    VSelect: {
      variant: "outlined",
      density: "comfortable",
      color: "primary",
    },
  },
});
