var imc = new Vue({
  el: '#imc',

  data:{
    poids: 0,
    taille: 0,
    res: 0
  },

  methods:{
    calcul: function(){
      this.poids = document.getElementById("poids").value;
      this.taille = document.getElementById("taille").value;
      this.res = this.poids/((this.taille/100)^2);
      alert(`Votre IMC est de ${this.res}`);
    }
  }
})
