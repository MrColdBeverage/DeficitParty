PARTY_CONTROL_CALLBACK="""
var button = radio.active;
console.log("--Running JS Callback--");

if (button == '0') {
    var source = deficit_cds.data;
    for (var i=0; i < source.color.length; i++) {
        if(source.DemSenateSeats[i]>50 && source.DemHouseSeats[i]>217 && source.DemWhitehouse[i]==1 ) 
        { 
            source.color[i]='blue'; 
        }
        else if(source.DemSenateSeats[i]<50 && source.DemHouseSeats[i]<217 && source.DemWhitehouse[i]==0)
        { 
            source.color[i]='red'; 
        }
        else
        { 
            source.color[i]='green' 
        }
    }
    deficit_cds.change.emit();
}
if (button == '1') {
    var source = deficit_cds.data;
    for (var i=0; i < source.color.length; i++) {
        if(source.DemSenateSeats[i]>50 && source.DemWhitehouse[i]==1 ) 
        { 
            source.color[i]='blue'; 
        }
        else if(source.DemSenateSeats[i]<50 && source.DemWhitehouse[i]==0)
        { 
            source.color[i]='red'; 
        }
        else
        { 
            source.color[i]='green' 
        }
    }
    deficit_cds.change.emit();
}
if (button == '2') {
    var source = deficit_cds.data;
    for (var i=0; i < source.color.length; i++) {
        if(source.DemHouseSeats[i]>217 && source.DemWhitehouse[i]==1 ) 
        { 
            source.color[i]='blue'; 
        }
        else if(source.DemHouseSeats[i]<217 &&source.DemWhitehouse[i]==0)
        { 
            source.color[i]='red'; 
        }
        else
        { 
            source.color[i]='green' 
        }
    }
    deficit_cds.change.emit();
}
"""