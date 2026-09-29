// Space80 R2 (apollo80_r2) - LED map and indicators.
// 87x WS2812 chain on B9, GRB, bitbang.
//
// Physical LED layout (from per-LED calibration):
//   0-5   badge strip (top of keyboard), left to right
//   6-35  rear-center -> CCW via left side -> left-front corner
//   36-53 bottom (front/under) edge, left to right
//   54-86 right-front corner -> CCW via right side -> rear-center
//   86 is physically adjacent to 6 at the rear-center seam
//
// Coordinate mapping:
//   x = physical horizontal position  -> used by *_left_right effects
//   y = ring arc-length from the seam -> used by *_up_down effects
//     (ring LEDs 6-86, i = idx-6: y = round(min(i, 80-i) * 64 / 40);
//      y = 0 at the seam between 86 and 6, y = 64 at the bottom center, LED 46)
// The seam LEDs 6 (x=112) and 86 (x=116) are adjacent in x, so left/right
// effects are continuous across the seam. Up/down effects start at the seam
// and merge symmetrically at the bottom center.
// Badge LEDs 0-5 keep their physical position and take part in the effects;
// they are only overridden (white) by the Caps Lock indicator below.

#include "quantum.h"

#ifdef RGB_MATRIX_ENABLE
led_config_t g_led_config = { {
    { NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED },
    { NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED },
    { NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED },
    { NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED },
    { NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED },
    { NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED, NO_LED },
}, {
    {150, 14}, {158, 14}, {166, 14}, {174, 14}, {182, 14}, {190, 14},
    {112, 0}, {106, 2}, {101, 3}, {95, 5}, {89, 6}, {84, 8},
    {78, 10}, {72, 11}, {67, 13}, {61, 14}, {55, 16}, {50, 18},
    {44, 19}, {38, 21}, {33, 22}, {27, 24}, {22, 26}, {16, 27},
    {10, 29}, {5, 30}, {4, 32}, {4, 34}, {4, 35}, {4, 37},
    {4, 38}, {4, 40}, {4, 42}, {4, 43}, {4, 45}, {4, 46},
    {14, 48}, {26, 50}, {37, 51}, {49, 53}, {60, 54}, {72, 56},
    {83, 58}, {95, 59}, {106, 61}, {118, 62}, {129, 64}, {141, 62},
    {152, 61}, {164, 59}, {175, 58}, {187, 56}, {198, 54}, {210, 53},
    {220, 51}, {220, 50}, {220, 48}, {220, 46}, {220, 45}, {220, 43},
    {220, 42}, {220, 40}, {220, 38}, {220, 37}, {220, 35}, {220, 34},
    {216, 32}, {211, 30}, {206, 29}, {201, 27}, {196, 26}, {191, 24},
    {186, 22}, {181, 21}, {176, 19}, {171, 18}, {166, 16}, {161, 14},
    {156, 13}, {151, 11}, {146, 10}, {141, 8}, {136, 6}, {131, 5},
    {126, 3}, {121, 2}, {116, 0}
}, {
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2
} };

// Caps Lock indicator: light the badge strip (LEDs 0-5) in white.
// Not locked: badge LEDs take part in the normal rgb_matrix effect.
bool rgb_matrix_indicators_advanced_kb(uint8_t led_min, uint8_t led_max) {
    if (!rgb_matrix_indicators_advanced_user(led_min, led_max)) {
        return false;
    }
    if (host_keyboard_led_state().caps_lock) {
        for (uint8_t i = 0; i <= 5; i++) {
            if (i >= led_min && i < led_max) {
                rgb_matrix_set_color(i, 0xFF, 0xFF, 0xFF);
            }
        }
    }
    return true;
}
#endif
