use std::fmt::Debug;

#[derive(PartialEq, Eq)]
pub enum ModuleState {
    Broadcaster,
    FlipFlop(bool),
    Conjunction(u64),
    Output,
}

impl ModuleState {
    pub fn new_broadcaster() -> Self {
        Self::Broadcaster
    }

    pub fn new_flipflop() -> Self {
        Self::FlipFlop(false)
    }

    pub fn new_conjunction() -> Self {
        Self::Conjunction(!0u64)
    }

    pub fn new_output() -> Self {
        Self::Output
    }

    pub fn connect_source_modules(&mut self, source_modules: &[usize]) {
        match self {
            Self::Conjunction(memory) => {
                for &source_module in source_modules {
                    *memory &= !(1u64 << source_module);
                }
            }
            _ => (),
        }
    }

    pub fn reset(&mut self, source_modules: &[usize]) {
        match self {
            Self::FlipFlop(is_on) => *is_on = false,
            Self::Conjunction(memory) => {
                *memory = !0u64;
                self.connect_source_modules(source_modules);
            }
            _ => (),
        }
    }

    pub fn handle_pulse(&mut self, source_module: usize, pulse: bool) -> Option<bool> {
        match self {
            Self::Broadcaster => Some(pulse),
            Self::FlipFlop(is_on) => {
                if pulse {
                    None
                } else {
                    *is_on = !*is_on;
                    Some(*is_on)
                }
            }
            Self::Conjunction(memory) => {
                if pulse {
                    *memory |= 1u64 << source_module;
                } else {
                    *memory &= !(1u64 << source_module);
                }
                Some(!(*memory == !0u64))
            }
            Self::Output => None,
        }
    }
}

impl Debug for ModuleState {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::Broadcaster => write!(f, "Broadcaster"),
            Self::FlipFlop(is_on) => write!(f, "FlipFlop({})", *is_on),
            Self::Conjunction(memory) => write!(f, "Conjunction({:b})", *memory),
            Self::Output => write!(f, "Output"),
        }
    }
}
