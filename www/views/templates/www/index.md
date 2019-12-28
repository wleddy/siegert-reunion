{% from '_mapping_helpers.html' import directions_snippet %}

## Welcome!

The Siegert's are having another family reunion hosted by Carol & John Roehrig II 
and their family in Houston Texas.

### When

July 31 thru August 2, 2020

### Where

Headquarters for the event will be at:

>	Spring Creek Oaks Clubhouse II  
>	6002 Bur Oak Drive  
>	Houston, TX 77379  
>	*web site:* [www.springcreekoaks.org](http://www.springcreekoaks.org/)

{% set lat = 30.0377 %}
{% set lng = -95.5064 %}
{{ directions_snippet(lat,lng) }}

Carol & John's place is at:

>	6035 Spring Creek Ln.  
>	Houston, TX 77379

{% set lat = 30.0362 %}
{% set lng = -95.5075 %}
{{ directions_snippet(lat,lng) }}

### RSVP

Please [click here]({{ url_for("www.contact") }}) or call 
![a phone #]({{ url_for('static',filename='images/tpn.png') }})
to let us know if you are coming.

Also please [click here]({{ url_for('www.poll') }}) to tell us what you'd like. 
We have a few questions we'd like to ask you before you come so
we'll be sure to have your favorites. 