var imc = new Vue({
  el: '#imc',

  data:{
    poids: 0,
    taille: 0,
    res: 0,
    corpulence: "normal"
  },

  methods:{
    calcul: function(){
      this.poids = document.getElementById("poids").value;
      this.taille = (document.getElementById("taille").value)/100;
      this.res = (this.poids/(this.taille*this.taille)).toFixed(2);
      if( this.poids <= 0 || this.taille <= 0 )
        alert(`Veuillez indiquer correctement votre poids et votre taille!`);
      else
      	if( this.res < 18.5 )
      		this.corpulence = "maigre";
      	else if( this.res > 25 )
      		this.corpulence = "en surpoids";
        alert(`Votre IMC est de ${this.res}, vous êtes ${this.corpulence}`);
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
