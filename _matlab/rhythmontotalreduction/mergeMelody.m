function [listOfRhythms, mel, tr] = mergeMelody(foldName, filName)

% load melodies
melF = sprintf('.\\melodies\\%s\\%s', foldName, filName);

fid = fopen(melF,'rt');
mel = textscan(fid,'%s %s %s','Delimiter','\t');
fclose(fid);

% load total reduction
trF = sprintf('.\\mergedTotalRedMeasures\\%s\\%s.csv', foldName, filName);

fid = fopen(trF,'rt');
tr = textscan(fid,'%s %s','Delimiter',';');
fclose(fid);

listOfRhythms = cell(length(mel{1,1}),4);

for i = 1:length(mel{1,1})
    if strcmp(mel{1,1}{i}, 'TS') || strcmp(mel{1,1}{i}, 'Grp')
        listOfRhythms{i,1} = mel{1,1}{i};
        listOfRhythms{i,2} = mel{1,2}{i};
    else
        listOfRhythms{i,1} = mel{1,1}{i};
        listOfRhythms{i,2} = tr{1,2}{i};
        listOfRhythms{i,3} = mel{1,2}{i};
        listOfRhythms{i,4} = mel{1,3}{i};
    end
end

cell2csv(strcat(filName,'.csv'), listOfRhythms, ';');
movefile(strcat(filName,'.csv'), ...
    sprintf('.\\mergedMelodies\\%s',foldName));

end