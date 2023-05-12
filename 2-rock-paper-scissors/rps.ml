type throw = Rock | Paper | Scissors

let score (yours : throw) (opponents : throw) : int =
  let shape_score = match yours with Rock -> 1 | Paper -> 2 | Scissors -> 3 in
  match (yours, opponents) with
  (* draws *)
  | Rock, Rock | Paper, Paper | Scissors, Scissors -> 3 + shape_score
  (* you win *)
  | Rock, Scissors | Paper, Rock | Scissors, Paper -> 6 + shape_score
  (* otherwise you lose *)
  | _, _ -> shape_score

(* Source: https://www.reddit.com/r/ocaml/comments/z6ws71/comment/j0ui7us/ *)
let read_lines file =
  In_channel.with_open_text file In_channel.input_all
  |> String.split_on_char '\n'

let str_to_throw (s : string) : throw =
  match s with
  | "A" | "X" -> Rock
  | "B" | "Y" -> Paper
  | "C" | "Z" -> Scissors
  | _ -> raise (Invalid_argument "guide contains invalid instructions")

let guide_to_throws (guide : string list) : (throw * throw) list =
  let line_to_throws l =
    match String.split_on_char ' ' l with
    | [] | _ :: [] | _ :: _ :: _ :: _ ->
        raise (Invalid_argument "line must contain exactly two entries")
    | [ opp; self ] -> (str_to_throw opp, str_to_throw self)
  in
  List.map line_to_throws guide

let total_score (guide : string list) : int =
  (* Order doesn't matter, because addition is commutative, so we might as
   * well use the tail-recursive rev_map in place of map *)
  let scores =
    List.rev_map (fun (opp, you) -> score you opp) (guide_to_throws guide)
  in
  List.fold_left ( + ) 0 scores

(* Part Two *)
type outcome = Win | Loss | Draw

let str_to_outcome (s : string) : outcome =
  match s with
  | "X" -> Loss
  | "Y" -> Draw
  | "Z" -> Win
  | _ -> raise (Invalid_argument "no corresponding outcome")

let outcome_to_throw (opponents : throw) (intended : outcome) : throw =
  match opponents with
  | Rock -> (
      match intended with Win -> Paper | Draw -> Rock | Loss -> Scissors)
  | Paper -> (
      match intended with Win -> Scissors | Draw -> Paper | Loss -> Rock)
  | Scissors -> (
      match intended with Win -> Rock | Draw -> Scissors | Loss -> Paper)

let line_to_throw_and_outcome (l : string) : throw * outcome =
  match String.split_on_char ' ' l with
  | [] | _ :: [] | _ :: _ :: _ :: _ ->
      raise (Invalid_argument "line must contain exactly two entries")
  | [ opp; out ] -> (str_to_throw opp, str_to_outcome out)

let outcome_based_total_score (guide : string list) : int =
  List.rev_map line_to_throw_and_outcome guide
  |> List.rev_map (fun (opp, out) -> score (outcome_to_throw opp out) opp)
  |> List.fold_left ( + ) 0
