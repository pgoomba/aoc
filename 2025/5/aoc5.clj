#!/usr/bin/env bb

(ns aoc5
  (:require [clojure.string :as str]))

(defn parse-range [s]
  (mapv parse-long (str/split s #"-")))

(defn in-any-range? [ranges x]
  (some (fn [[a b]] (<= a x b)) ranges))

(defn count-fresh [ranges ingredients]
  (count (filter #(in-any-range? ranges %) ingredients)))

(defn collapse-ranges [ranges]
  (let [sorted (sort-by first ranges)]
    (reduce
     (fn [acc [start end]]
       (if (empty? acc)
         [[start end]]
         (let [[last-start last-end] (peek acc)]
           (if (<= start (inc last-end))
             (conj (pop acc) [last-start (max last-end end)])
             (conj acc [start end])))))
     []
     sorted)))

(defn range-size [[a b]]
  (inc (- b a)))

(defn count-in-ranges [ranges]
  (->> ranges
       collapse-ranges
       (map range-size)
       (reduce +)))

(defn parse-input [path]
  (let [[ranges ingredients]
        (->> path
             slurp
             str/split-lines
             (split-with (complement str/blank?)))]
    {:ranges      (map parse-range ranges)
     :ingredients (map parse-long (rest ingredients))}))

(defn -main []
  (let [{:keys [ranges ingredients]} (parse-input "input.txt")]
    (println "Step1:" (count-fresh ranges ingredients))
    (println "Step2:" (count-in-ranges ranges))))

(-main)
