function listOfOnsets = totalReductionOfFIle(foldName, filName)

tmpF = sprintf('./output/%s/%s', foldName, filName);

fid = fopen(tmpF,'rt');
tmp = textscan(fid,'%s %s %s %s %s','Delimiter',';');
fclose(fid);

onsets = tmp{1,1};
chords = tmp{1,2};
chordsRed = tmp{1,3};

tmpKey = 0;
tmpMode = [0, 2, 4, 5, 7, 9, 11];

listOfOnsets = cell(0,2);

prevChord = [];

for i = 1:length(onsets)
    if strcmp(onsets{i}, 'tonality')
        tmpKey = str2num(chords{i});
        tmpMode = str2num(chordsRed{i});
        prevChord = [];
    elseif strcmp(onsets{i}, 'grouping')
        listOfOnsets{end+1,1} = 'Grp';
        listOfOnsets{end,2} = chords{i};
        prevChord = [];
    else
        if ~isempty(chordsRed{i})
            if ~isempty(prevChord)
                if ~isDelegateOf(str2num(chordsRed{i}), prevChord, ...
                        [tmpKey tmpMode]) & ...
                        ~isDelegatedBy(str2num(chordsRed{i}), prevChord, ...
                        [tmpKey tmpMode]) & ...
                        ~isequal(str2num(chordsRed{i}), prevChord)
                    listOfOnsets{end+1,1} = 'Chord';
                    listOfOnsets{end,2} = onsets{i};
                end
                prevChord = str2num(chordsRed{i});
            else
                if ~isempty(str2num(chordsRed{i}))
                    listOfOnsets{end+1,1} = 'Chord';
                    listOfOnsets{end,2} = onsets{i};
                    prevChord = str2num(chordsRed{i});
                end
            end
        end
    end
    
end

cell2csv(strcat(filName,'.csv'), listOfOnsets, ';');
movefile(strcat(filName,'.csv'), sprintf('./totalRed/%s',foldName));

end