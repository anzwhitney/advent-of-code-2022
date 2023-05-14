module type INTERVAL = sig
  type point
  type interval

  (* Contains is symmetric, i.e., also covers "contained by". *)
  type relation = Disjoint | Overlaps | Contains

  (* Returns the interval between two points. *)
  val interval : point -> point -> interval

  (* Returns the endpoints of an interval as a pair with the first point less
   * than the second. *)
  val endpoints : interval -> point * point

  (* Returns the relation holding between two intervals. *)
  val relation : interval -> interval -> relation

  (* Returns the union of two intervals, i.e., the smallest interval containing
   * both intervals. *)
  val union : interval -> interval -> interval

  (* Returns the intersection of two intervals. Undefined if the intervals are
   * disjoint. *)
  val intersection : interval -> interval -> interval option
end

module type COMPARABLE = sig
  type t
  type order = Less | Equal | Greater

  val compare : t -> t -> order
end

module MakeInterval (Point : COMPARABLE) : INTERVAL with type point = Point.t =
struct
  type point = Point.t
  type interval = point * point
  type relation = Disjoint | Overlaps | Contains

  let interval (p1 : point) (p2 : point) : interval =
    match Point.compare p1 p2 with
    | Less -> (p1, p2)
    | Equal -> (p1, p2)
    | Greater -> (p2, p1)

  let endpoints (i : interval) : point * point = i

  (* Assumes that all intervals are open, i.e., endpoints not included. *)
  let relation ((start1, end1) : interval) ((start2, end2) : interval) :
      relation =
    (* Whichever interval has the lesser start is A; the other is B. The cases
     * where start1 < start2 and start1 > start2 are therefore identical except
     * for which interval is A vs B. The start1 = start2 case is handled
     * separately without this helper function. *)
    let relation_nonshared_start eA sB eB =
      match Point.compare eA sB with
      | Less | Equal -> Disjoint (* sA--eA/sB... or sA--eA  sB... *)
      | Greater -> (
          (* sA--sB...eB... *)
          match Point.compare eA eB with
          | Less -> Overlaps (* sA--sB--eA--eB *)
          | Equal | Greater -> Contains)
      (* sA--sB...eB/eA or sA--sB...eB--eA *)
    in
    match Point.compare start1 start2 with
    | Equal -> (
        (* s1/s2-... *)
        match Point.compare end1 start2 with
        | Less ->
            raise (Failure "end of an interval cannot be less than its start")
        | Equal -> Disjoint
        (* s1/e1/s2... - disjoint because these are assumed to be open
         * intervals, and if s1=s2 and e1=s2, then s1=e1, so interval 1 is
         * empty. *)
        | Greater ->
            Contains
            (* s1/s2--e1--e2, s1/s2--e1/e2, or s1/s2--e2--e1 - in all these 
             * cases one interval contains the other. *))
    | Less -> relation_nonshared_start end1 start2 end2
    | Greater -> relation_nonshared_start end2 start1 end1

  let union ((start1, end1) : interval) ((start2, end2) : interval) : interval =
    let outer_end =
      match Point.compare end1 end2 with
      | Less -> end2
      | Equal | Greater -> end1
    in
    match Point.compare start1 start2 with
    | Less | Equal -> (start1, outer_end)
    | Greater -> (start2, outer_end)

  let intersection (i1 : interval) (i2 : interval) : interval option =
    let outer_point (ord : Point.order) (p1 : point) (p2 : point) =
      match Point.compare p1 p2 with
      | Less -> if ord = Less then p1 else p2
      | Equal -> p1 (* arbitrarily pick p1, since p1=p2 *)
      | Greater -> if ord = Greater then p1 else p2
    in
    let (s1, e1), (s2, e2) = (i1, i2) in
    match relation i1 i2 with
    | Disjoint -> None
    | Overlaps | Contains ->
        Some (outer_point Greater s1 s2, outer_point Less e1 e2)
end

module DiscreteTime : COMPARABLE with type t = int = struct
  type t = int
  type order = Less | Equal | Greater

  let compare (t1 : t) (t2 : t) : order =
    if t1 < t2 then Less else if t1 > t2 then Greater else Equal
end

module DiscreteTimeInterval = MakeInterval (DiscreteTime)
