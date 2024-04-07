use std::{collections::HashMap, vec};

pub enum Module {
    BroadcasterModule(ModuleBase),
    FlipFlopModule(ModuleBase, bool),
    ConjunctionModule(ModuleBase, HashMap<String, bool>),
}

pub struct ModuleBase {
    name: String,
    destination_modules: Vec<String>,
}

impl Module {
    pub fn new_broadcaster_module(name: String, destination_modules: Vec<String>) -> Self {
        Self::BroadcasterModule(ModuleBase {
            name,
            destination_modules,
        })
    }

    pub fn new_flipflop_module(name: String, destination_modules: Vec<String>) -> Self {
        Self::FlipFlopModule(
            ModuleBase {
                name,
                destination_modules,
            },
            false,
        )
    }

    pub fn new_conjunction_module(name: String, destination_modules: Vec<String>) -> Self {
        Self::ConjunctionModule(
            ModuleBase {
                name,
                destination_modules,
            },
            HashMap::new(),
        )
    }

    pub fn get_name(&self) -> &str {
        match self {
            Self::BroadcasterModule(base) => &base.name,
            Self::FlipFlopModule(base, _) => &base.name,
            Self::ConjunctionModule(base, _) => &base.name,
        }
    }

    pub fn get_destination_modules(&self) -> &[String] {
        match self {
            Self::BroadcasterModule(base) => &base.destination_modules,
            Self::FlipFlopModule(base, _) => &base.destination_modules,
            Self::ConjunctionModule(base, _) => &base.destination_modules,
        }
    }

    pub fn set_source_modules(&mut self, source_modules: Vec<String>) {
        match self {
            Self::BroadcasterModule(_) => (),
            Self::FlipFlopModule(_, _) => (),
            Self::ConjunctionModule(_, memory) => {
                for source_module in source_modules {
                    memory.insert(source_module, false);
                }
            }
        }
    }

    pub fn handle_pulse(
        &mut self,
        source_module: &str,
        pulse: bool,
    ) -> Vec<(String, bool, String)> {
        match self {
            Self::BroadcasterModule(base) => base
                .destination_modules
                .iter()
                .cloned()
                .map(|dm: String| (base.name.clone(), pulse, dm))
                .collect(),
            Self::FlipFlopModule(base, is_on) => {
                if pulse {
                    vec![]
                } else {
                    *is_on = !*is_on;
                    base.destination_modules
                        .iter()
                        .cloned()
                        .map(|dm: String| (base.name.clone(), *is_on, dm))
                        .collect()
                }
            }
            Self::ConjunctionModule(base, memory) => {
                let temp = memory.get_mut(source_module).unwrap();
                *temp = pulse;
                let pulse_to_send = !memory.values().all(|b: &bool| *b);
                base.destination_modules
                    .iter()
                    .cloned()
                    .map(|dm: String| (base.name.clone(), pulse_to_send, dm))
                    .collect()
            }
        }
    }
}
