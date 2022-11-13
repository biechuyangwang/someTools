from mido import Message, MidiFile, MidiTrack

bpm=56 # 对应meta_time:500，但是ACE中对齐的meta_time:480
meta_time=int(60*1000/bpm)  # 60*1000/bpm 一拍时值
base_note=60
delay = 0 # 出现休止符，控制下个音符的开始时间（相对）

notestr = "0 2 1 6- 1 1 6- 1 1 6- 1 6- 5-"
major_notes = [0, 2, 2, 1, 2, 2, 2, 1]
durstr= "1 1 1 1 2 1 1 2 1 1 1 1 2" # 16分音符为基础单位
major_dur = 4 # 一拍等于4个16分音符


def string2notelist(str, base_note, major_notes):
    notelist = []
    for note in str.split():
        if len(note) == 1:
            if note == "0": # 处理休止符
                notelist.append(0)
            else: notelist.append(base_note + sum(major_notes[0:int(note)]))
        else: # 每一个“-”低8度，每一个“.”升8度
            if note[1]=="-":
                notelist.append(base_note - (len(note)-1)*12 + sum(major_notes[0:int(note[0])]))
            elif note[1]==".":
                notelist.append(base_note + (len(note)-1)*12 + sum(major_notes[0:int(note[0])]))
    return notelist

def string2durlist(str, meta_time, major_dur):
    durlist = []
    for dur in str.split():
        durlist.append(int(meta_time*int(dur)/major_dur))
    return durlist


def addNote(note, durTime, track=0, velocity=1.0, channel=0):
    global delay
    track.append(Message('note_on', note=note, velocity=round(64 * velocity), \
                time=delay, channel=channel))
    track.append(Message('note_off', note=note, velocity=round(64 * velocity), \
                time=durTime, channel=channel))

def addNotes2Track(notelist, durlist, track=0, velocity=1.0, channel=0):
    if len(notelist) != len(durlist):
        print("note和时值数量不匹配！")
        exit(1)
    for note,durTime in zip(notelist,durlist):
        global delay
        addNote(note, durTime, track, velocity, channel)
        delay = 0 # 每次重置延迟
        if note==0:
            delay = durTime

def outMideFile(name,notelist,durlist,program=0):
    mid = MidiFile()  # 创建MidiFile对象
    track = MidiTrack()  # 创建音轨
    mid.tracks.append(track)  # 把音轨加到MidiFile对象中
    track.append(Message('program_change', channel=0, program=program, time=0)) # 确定这个轨道的乐器，prpgram是声学钢琴
    addNotes2Track(notelist,durlist,track)
    mid.save(f'{name}.mid')

def main(name):
    notelist = string2notelist(notestr, base_note, major_notes)
    durlist = string2durlist(durstr,meta_time, major_dur)
    print(notelist)
    print(durlist)

    outMideFile(name,notelist,durlist,0)

if __name__ == "__main__":
    name = "青花瓷"
    main(name)

# input
# notestr = "0 2 1 6- 1 1 6- 1 1 6- 1 6- 5-"
# major_notes = [0, 2, 2, 1, 2, 2, 2, 1]
# durstr= "1 1 1 1 2 1 1 2 1 1 1 1 2" # 16分音符为基础单位

# notelist and drlist
# [0, 62, 60, 57, 60, 60, 57, 60, 60, 57, 60, 57, 55]
# [267, 267, 267, 267, 535, 267, 267, 535, 267, 267, 267, 267, 535]

