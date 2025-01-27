(deftemplate MAIN::tlvl
   (slot value (allowed-values normal medium high)))

(deftemplate MAIN::start
   (slot type (allowed-values fever gradual)))

(deftemplate MAIN::diagnosis
   (slot result (allowed-values healthy vri flu undefine)))

(defrule MAIN::get-temperature
   (initial-fact) 
   =>
   (printout t "Введите вашу текущую температуру тела: " crlf)
   (assert (t (read))))

(defrule MAIN::classify-tlvl-high
   (t ?t)
   (test (> ?t 38.3))
   =>
   (assert (tlvl (value high)))
   (printout t "Уровень вашей текущей температуры тела: Высокий!" crlf))

(defrule MAIN::classify-tlvl-medium
   (t ?t)
   (test (>= ?t 37.2))
   (test (<= ?t 38.3))
   =>
   (assert (tlvl (value medium)))
   (printout t "Уровень вашей текущей температуры тела: Завышенный!." crlf))

(defrule MAIN::classify-tlvl-normal
   (t ?t)
   (test (< ?t 37.2))
   =>
   (assert (tlvl (value normal)))
   (printout t "Уровень вашей текущей температуры тела: В норме!." crlf))

(defrule MAIN::prompt-start-for-medium-or-high
   (or  (tlvl (value medium))
        (tlvl (value high)))
   (not (start))
   =>
   (printout t "Как проходила ваша болезнь - лихорадочно или постепенно? (fever or gradual): " crlf)
   (assert (start (type (read)))))

(defrule MAIN::undefine_diagnosis
   (tlvl (value medium))
   (start (type fever))
   =>
   (assert (diagnosis (result undefine)))
   (printout t "По всем показателям мы не можем определить ваш диагноз." crlf))

(defrule MAIN::fludiagnosis
   (tlvl (value high))
   (start (type fever))
   =>
   (assert (diagnosis (result flu)))
   (printout t "По всем показателям ваш диагноз - это ГРИПП." crlf))


(defrule MAIN::undefine_diagnosis_2
   (tlvl (value high))
   (start (type gradual))
   =>
   (assert (diagnosis (result undefine)))
   (printout t "По всем показателям мы не можем определить ваш диагноз." crlf))


(defrule MAIN::vridiagnosis
   (tlvl (value medium))
   (start (type gradual))
   =>
   (assert (diagnosis (result vri)))
   (printout t "По всем показателям ваш диагноз - это ОРВИ." crlf))

(defrule MAIN::healthydiagnosis
   (tlvl (value normal))
   =>
   (assert (diagnosis (result healthy)))
   (printout t "По всем показателям вы здоровы!" crlf))

(defrule MAIN::ensure-initial-fact
   (not (initial-fact))
   =>
   (assert (initial-fact)))

