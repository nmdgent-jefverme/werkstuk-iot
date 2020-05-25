const dbConfig = {
  collection: 'raspberry_collection',
  document: 'jefvermepi_doc'
};

const firebaseConfig = {
  apiKey: "AIzaSyCmHMLkNDpZONyPljpNvVFdUMhBkBNoI_E",
  authDomain: "labo-iot.firebaseapp.com",
  databaseURL: "https://labo-iot.firebaseio.com",
  projectId: "labo-iot",
  storageBucket: "labo-iot.appspot.com",
  messagingSenderId: "411189027368",
  appId: "1:411189027368:web:522e0093803fbefa3e8b1d"
};

const app = {
  async init() {
      // initialiseer de firebase app
      firebase.initializeApp(firebaseConfig);
      this._db = firebase.firestore();
      this.cacheDOMElements();
      await this.createDOMElements();
      await this.readSensorData();

      this._matrix = {
          isOn: false, color: {value: '#000000', type: 'hex'}
      };
  },
  async createDOMElements(){
      this._db.collection('lights')
      .onSnapshot((doc) => {
          this.$container.innerHTML = '';
          doc.forEach((light)=> {
              this.createCard(light.data(), light.id);
          })
      })
  },
  createCard(data, id) {
      let div = document.createElement('div');
      div.className = 'item';
      let p = document.createElement('p');
      p.innerText = data.naam;
      let img = document.createElement('img');
      if(data.active) {
          img.src = './assets/images/lightOn.png';
      } else {
          img.src = './assets/images/lightOff.png';
      }
      img.addEventListener('click', () => {
          this.toggleLight(id, data.active);
      })
      div.appendChild(p);
      div.appendChild(img);
      this.$container.appendChild(div);
  },
  toggleLight(id, active) {
      this._db.collection('lights').doc(id)
          .set(
              {active: !active},
              {merge: true}
          );
  },
  cacheDOMElements() {
      this.$container = document.getElementById('lightsContainer');
      this.$temperature = document.getElementById('temperature');
      this.$humidity = document.getElementById('humidity');
      this.$cpuTemp = document.getElementById('cpuTemp');
  },
  readDB() {
      console.log(document.getElementsByClassName('items'));
  },
  readSensorData() {
      this._db.collection('sensoren').doc('tempEnHumidity')
      .onSnapshot((doc) => {
          this.$temperature.innerText = `${parseFloat(doc.data().temperature).toFixed(2)}°C`;
          this.$humidity.innerText = `${parseFloat(doc.data().humidity).toFixed(2)}%`;
      })
      this._db.collection('sensoren').doc('cpuTemp')
      .onSnapshot((doc) => {
          console.log(doc.data());
          this.$cpuTemp.innerText = `${doc.data().temp}°C`;
      })
  }
}

app.init();
