mod module_state;

use self::module_state::ModuleState;
use std::collections::{HashMap, VecDeque};
use std::fmt::Debug;

#[derive(Debug)]
pub struct Circuit {
    #[allow(dead_code)]
    module_names: Vec<String>,
    source_modules: Vec<Vec<usize>>,
    destination_modules: Vec<Vec<usize>>,
    module_states: Vec<ModuleState>,
}

impl Circuit {
    pub fn new(
        module_prefixes: Vec<String>,
        module_names_raw: Vec<String>,
        destination_modules_raw: Vec<Vec<String>>,
    ) -> Self {
        let mut module_names = vec!["broadcaster".to_string()];
        let mut module_name_to_index = HashMap::new();
        module_name_to_index.insert("broadcaster".to_string(), 0usize);
        let mut module_states = vec![ModuleState::new_broadcaster()];
        for (module_prefix, module_name) in module_prefixes
            .into_iter()
            .zip(module_names_raw.iter().cloned())
        {
            match module_prefix.as_str() {
                "%" => {
                    module_name_to_index.insert(module_name.clone(), module_names.len());
                    module_names.push(module_name);
                    module_states.push(ModuleState::new_flipflop());
                }
                "&" => {
                    module_name_to_index.insert(module_name.clone(), module_names.len());
                    module_names.push(module_name);
                    module_states.push(ModuleState::new_conjunction());
                }
                _ => (),
            }
        }
        for destination_module_names in destination_modules_raw.iter() {
            for destination in destination_module_names.iter() {
                if !module_name_to_index.contains_key(destination) {
                    module_name_to_index.insert(destination.to_string(), module_names.len());
                    module_names.push(destination.to_string());
                    module_states.push(ModuleState::new_output())
                }
            }
        }
        let mut destination_modules = vec![vec![]; module_names.len()];
        for (module_name, destination_module_names) in module_names_raw
            .into_iter()
            .zip(destination_modules_raw.into_iter())
        {
            let destination_module_indices: Vec<_> = destination_module_names
                .into_iter()
                .map(|name| module_name_to_index[&name])
                .collect();
            destination_modules[module_name_to_index[&module_name]]
                .extend(destination_module_indices);
        }
        let mut source_modules = vec![vec![]; module_names.len()];
        for (i, destinations) in destination_modules.iter().enumerate() {
            for &destination in destinations {
                source_modules[destination].push(i);
            }
        }
        for (i, sources) in source_modules.iter().enumerate() {
            module_states[i].connect_source_modules(sources);
        }
        Self {
            module_names,
            source_modules,
            destination_modules,
            module_states,
        }
    }

    pub fn reset(&mut self) {
        for (module_state, sources) in self
            .module_states
            .iter_mut()
            .zip(self.source_modules.iter())
        {
            module_state.reset(sources);
        }
    }

    pub fn handle_pulse(
        &mut self,
        source: usize,
        pulse: bool,
        destination: usize,
    ) -> Vec<(usize, bool, usize)> {
        if let Some(result) = self.module_states[destination].handle_pulse(source, pulse) {
            self.destination_modules[destination]
                .iter()
                .map(|&dest| (destination, result, dest))
                .collect()
        } else {
            vec![]
        }
    }

    pub fn press_button(&mut self) -> bool {
        let mut pulse_queue: VecDeque<_> = vec![(!0usize, false, 0usize)].into();
        while !pulse_queue.is_empty() {
            let (source, pulse, dest) = pulse_queue.pop_front().unwrap();
            if self.module_states[dest] == ModuleState::Output && !pulse {
                return true;
            }
            pulse_queue.extend(self.handle_pulse(source, pulse, dest))
        }
        false
    }

    pub fn press_button_and_count_pulses(&mut self) -> (usize, usize) {
        let mut pulse_queue: VecDeque<_> = vec![(!0usize, false, 0usize)].into();
        let mut low_pulse_count = 0;
        let mut high_pulse_count = 0;
        while !pulse_queue.is_empty() {
            let (source, pulse, dest) = pulse_queue.pop_front().unwrap();
            if pulse {
                high_pulse_count += 1;
            } else {
                low_pulse_count += 1;
            }
            pulse_queue.extend(self.handle_pulse(source, pulse, dest))
        }
        (low_pulse_count, high_pulse_count)
    }
}
