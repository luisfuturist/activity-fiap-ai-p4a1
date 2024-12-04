// Wokwi Custom Chip - For docs and examples see:
// https://docs.wokwi.com/chips-api/getting-started
//
// SPDX-License-Identifier: MIT
// Copyright 2023 Luis Domínguez

#include "wokwi-api.h"
#include <stdio.h>
#include <stdlib.h>

typedef struct {
  pin_t pin_collector;
  pin_t pin_emitter;
  pin_t pin_base;
} chip_state_t;

static void chip_pin_change(void *user_data, pin_t pin, uint32_t value) {
  chip_state_t *chip = (chip_state_t*)user_data;

  if (value == HIGH && pin_read(chip->pin_emitter) == LOW) {
    pin_mode(chip->pin_collector, INPUT);
  } else {
    pin_mode(chip->pin_collector, OUTPUT);
  }
}

void chip_init(void) {
  chip_state_t *chip = malloc(sizeof(chip_state_t));
  chip->pin_collector = pin_init("COLLECTOR", OUTPUT);
  chip->pin_emitter = pin_init("EMITTER", INPUT);
  chip->pin_base = pin_init("BASE", INPUT);

  const pin_watch_config_t config = {
    .edge = BOTH,
    .pin_change = chip_pin_change,
    .user_data = chip,
  };
  pin_watch(chip->pin_base, &config);
}