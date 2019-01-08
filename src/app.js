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
      this.res = (this.poids/((this.taille/100)^2)).toFixed(2);
      if( this.poids.length == 0 || this.taille.length == 0 )
        alert(`Veuillez indiquer correctement votre poids et votre taille!`);
      else
        alert(`Votre IMC est de ${this.res}`);
    }
  }
})

var dej = new Vue({
  el: '#dej',

  data:{
    poids: 0,
    taille: 0,


    res: 0
  },

  methods:{
    ajouteActivite: function( uneActivite ){

    }
  }
})
