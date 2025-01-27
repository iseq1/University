 (deftemplate MAIN::city
   (slot value (allowed-values Kazan)))

 (deftemplate MAIN::w
   (slot type (allowed-values sunny)))
 
 (defrule MAIN::classify-tlvl-high
    (initial-fact) 
    =>
    (assert (city (value Kazan)))
    (assert (w (value sunny)))
)

 (defrule MAIN::test 
    (weather in ?city is ?w)
     => 
    (printout t ?city " - " ?w crlf)
)

