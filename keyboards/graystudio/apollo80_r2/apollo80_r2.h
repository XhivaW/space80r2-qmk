#pragma once

#include "quantum.h"

// Runtime LED region switches (bitmask, 1 = region hidden).
#define LED_REGION_BADGE 0x01  // badge strip 0-5
#define LED_REGION_BOTTOM 0x02 // bottom edge 36-53
#define LED_REGION_SIDES 0x04  // side bands 6-35 + 54-86

// Toggle a region and persist the mask in EEPROM.
void led_region_toggle(uint8_t region);
