#![allow(non_snake_case)]
mod module;

use module::Module;
use regex::Regex;
use std::collections::{HashMap, VecDeque};
use std::fs;
use std::path::Path;

fn main() {
    let mut modules = parse_file("input");
    let mut button_presses = 0;
    let mut is_done = false;
    while !is_done {
        let (_, _, temp) = press_button(&mut modules, "rx");
        is_done = temp;
        button_presses += 1;
        if button_presses % 1000000 == 0 {
            println!("{button_presses}");
        }
    }
    println!("{button_presses}")

    /*let mut low_pulse_count = 0;
    let mut high_pulse_count = 0;
    for _ in 0..1000 {
        let (dl, dh, _) = press_button(&mut modules, "output");
        low_pulse_count += dl;
        high_pulse_count += dh;
        button_presses += 1;
    }
    println!("{low_pulse_count} {high_pulse_count} {button_presses}");*/
}

/*lazy_static! {
    static ref RE = Regex::new("(broadcaster|%|&)([a-z]*) -> ([a-z, ]+)").unwrap();
}*/

fn parse_file(filename: impl AsRef<Path>) -> HashMap<String, Module> {
    let mut modules: HashMap<String, Module> = HashMap::new();
    for line in fs::read_to_string(filename).unwrap().lines() {
        let module = parse_line(line);
        modules.insert(module.get_name().to_string(), module);
    }
    connect_source_modules(&mut modules);
    modules
}

fn parse_line(line: &str) -> Module {
    let RE = Regex::new("(broadcaster|%|&)([a-z]*) -> ([a-z, ]+)").unwrap();
    let captures = RE.captures(line).unwrap();
    let module_prefix = captures.get(1).unwrap().as_str();
    let module_name = captures.get(2).unwrap().as_str();
    let destination_modules = captures.get(3).unwrap().as_str();
    let destination_modules: Vec<String> = destination_modules
        .split(", ")
        .map(|s| s.to_string())
        .collect();
    if module_prefix == "broadcaster" {
        Module::new_broadcaster_module("broadcaster".to_string(), destination_modules)
    } else if module_prefix == "%" {
        Module::new_flipflop_module(module_name.to_string(), destination_modules)
    } else {
        Module::new_conjunction_module(module_name.to_string(), destination_modules)
    }
}

fn connect_source_modules(modules: &mut HashMap<String, Module>) {
    let mut source_modules: HashMap<String, Vec<String>> = modules
        .iter()
        .map(|(name, _)| (name.clone(), vec![]))
        .collect();
    for module in modules.values() {
        for destination_module_name in module.get_destination_modules() {
            if modules.contains_key(destination_module_name) {
                source_modules
                    .get_mut(destination_module_name)
                    .unwrap()
                    .push(module.get_name().to_string())
            }
        }
    }
    for (module_name, source_modules) in source_modules.into_iter() {
        modules
            .get_mut(&module_name)
            .unwrap()
            .set_source_modules(source_modules);
    }
}

fn press_button(modules: &mut HashMap<String, Module>, watch_for: &str) -> (usize, usize, bool) {
    let mut pulse_queue: VecDeque<(String, bool, String)> =
        vec![("button".to_string(), false, "broadcaster".to_string())].into();
    let mut low_pulse_count = 0;
    let mut high_pulse_count = 0;
    let mut sent_to_watch_for = false;
    while !pulse_queue.is_empty() {
        let (source_module, pulse, destination_module) = pulse_queue.pop_front().unwrap();
        if destination_module == watch_for && !pulse {
            sent_to_watch_for = true;
        }
        if pulse {
            high_pulse_count += 1;
        } else {
            low_pulse_count += 1;
        }
        if modules.contains_key(&destination_module) {
            pulse_queue.extend(
                modules
                    .get_mut(&destination_module)
                    .unwrap()
                    .handle_pulse(&source_module, pulse),
            )
        }
    }
    (low_pulse_count, high_pulse_count, sent_to_watch_for)
}
