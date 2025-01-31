import i18n from "i18next";
import { initReactI18next } from "react-i18next";
import HttpApi from "i18next-http-backend";

i18n
  .use(HttpApi) 
  .use(initReactI18next)
  .init({
    fallbackLng: "en",
    lng: "en", 
    interpolation: {
      escapeValue: false, 
    },
    backend: {
      loadPath: "/locales/{{lng}}.json", 
    },
    debug: true, 
    react: {
      useSuspense: false, 
    },
  });

export default i18n;
