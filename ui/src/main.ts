import 'reflect-metadata';

import { createApp } from 'vue';
import { createPinia } from 'pinia';
import { createInjector } from '@/utils/di';
import vuetify from './plugins/vuetify';

import App from './App.vue';
import router from './router';
import { AppConfig } from '@/core/AppConfig';
import { ApiService } from '@/core/ApiService';
import { ClassifierApiService } from '@/classifier/ClassifierApiService';

import '@/scss/style.scss';

const injector = createInjector({
  services: [AppConfig, ApiService, ClassifierApiService],
});

// import { MockClassifierApiService } from '@/classifier/MockClassifierApiService';
// injector.set(ClassifierApiService, MockClassifierApiService);

(async () => {
  try {
    const config = injector.get(AppConfig);
    await config.init();

    const app = createApp(App);

    app.use(createPinia());
    app.use(router);
    app.use(injector);
    app.use(vuetify);

    app.mount('#app');
  } catch (e) {
    alert('Error: ' + e);
    setTimeout(() => {
      location.reload();
    }, 1000);
  }
})();
