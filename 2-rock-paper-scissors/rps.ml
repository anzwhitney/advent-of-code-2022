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
