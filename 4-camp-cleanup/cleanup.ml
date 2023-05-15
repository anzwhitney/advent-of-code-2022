(* TODO: factor this out into a util module to share between here and day 2
 * (and presumably any other days I end up using OCaml for) *)
(* Adapted from
 * https://www.reddit.com/r/ocaml/comments/z6ws71/comment/j0ui7us/ *)
let read_lines file =
  In_channel.with_open_text file In_channel.input_all
  |> String.split_on_char '\n'
  |> List.filter (fun s -> s <> "")

module Section : Interval.COMPARABLE with type t = int = struct
  type t = int
  type order = Less | Equal | Greater

  let compare (s1 : t) (s2 : t) : order =
    if s1 < s2 then Less else if s1 > s2 then Greater else Equal
end

module SI = Interval.MakeClosedInterval (Section)

(* Parse an input line of the form "A-B,C-D" into the intervals [A,B] and
 * [C,D]. *)
let string_to_intervals (s : string) : SI.interval * SI.interval =
  match String.split_on_char ',' s with
  | [] | _ :: [] | _ :: _ :: _ :: _ ->
    raise (Invalid_argument "Must have exactly two intervals per line")
  | [ first; second ] ->
    let interval substr =
      match String.split_on_char '-' substr with
      | [] | _ :: [] | _ :: _ :: _ :: _ ->
        raise
          (Invalid_argument "Must have exactly two endpoints per interval")
      | [ startpt; endpt ] -> SI.interval (int_of_string startpt) (int_of_string endpt)
    in
    (interval first, interval second)

let total_contained (include_overlaps: bool) (l : (SI.interval * SI.interval) list) : int =
  let count_contained acc (a, b) =
    match SI.relation a b with
    | Disjoint -> acc
    | Overlaps -> if include_overlaps then acc + 1 else acc
    | Contains -> acc + 1
  in
  List.fold_left count_contained 0 l


(* Run from command line *)
let usage_msg = "cleanup [-include_overlaps] <input_filename>"

let input_filename = ref ""

let include_overlaps = ref false

let anon_fun filename = input_filename := filename

let speclist = [("-include_overlaps", Arg.Set include_overlaps, "Count intervals that overlap as well as ones that are fully contained.")]

let () = Arg.parse speclist anon_fun usage_msg;
  let lines = read_lines !input_filename in
  let total = total_contained !include_overlaps (List.map string_to_intervals lines) in
  print_string "There are ";
  print_int total;
  print_string " assignment pairs where one range";
  if !include_overlaps then print_endline " overlaps the other."
  else print_endline " fully contains the other."
