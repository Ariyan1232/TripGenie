import { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  ActivityIndicator,
  Alert,
} from 'react-native';
import { Colors } from '../constants/colors';
import Button from '../components/Button';
import { addTraveler } from '../api/trips';

const AIRPORT_OPTIONS = ['JFK', 'LHR', 'NRT', 'CDG', 'BKK', 'SIN', 'LAX', 'DXB'];

export default function VoteScreen({ navigation, route }) {
  // Trip code can come from navigation params (if coming from Members screen)
  // or the user can type it in manually
  const [tripCode, setTripCode] = useState(route.params?.tripId || '');
  const [name, setName] = useState('');
  const [origin, setOrigin] = useState('');
  const [earliest, setEarliest] = useState('');
  const [latest, setLatest] = useState('');
  const [votes, setVotes] = useState([]);
  const [loading, setLoading] = useState(false);

  const toggleVote = (code) => {
    setVotes((prev) =>
      prev.includes(code) ? prev.filter((v) => v !== code) : [...prev, code]
    );
  };

  const handleJoin = async () => {
    if (!tripCode) {
      Alert.alert('Missing trip code', 'Please enter a trip code to join.');
      return;
    }
    if (!name || !origin || !earliest || !latest) {
      Alert.alert('Missing fields', 'Please fill in all fields.');
      return;
    }
    if (votes.length === 0) {
      Alert.alert('No destinations', 'Please vote for at least one destination.');
      return;
    }

    setLoading(true);
    try {
      await addTraveler(tripCode, {
        name,
        origin_airport: origin,
        earliest_departure: earliest,
        latest_return: latest,
        destination_votes: votes,
      });

      navigation.navigate('Members', {
        tripId: tripCode,
        tripName: 'Trip',
      });
    } catch (error) {
      Alert.alert(
        'Error',
        'Could not join trip. Check the trip code and try again.'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView style={styles.scroll} contentContainerStyle={styles.container}>

      <Text style={styles.heading}>Join a trip</Text>
      <Text style={styles.subheading}>
        Enter your trip code and details to join the group.
      </Text>

      {/* Trip code */}
      <Text style={styles.sectionLabel}>TRIP CODE</Text>
      <TextInput
        style={[styles.input, styles.codeInput]}
        placeholder="e.g. 28714f94"
        placeholderTextColor={Colors.textMuted}
        value={tripCode}
        onChangeText={setTripCode}
        autoCapitalize="none"
        autoCorrect={false}
      />

      {/* Personal details */}
      <Text style={styles.sectionLabel}>YOUR DETAILS</Text>
      <TextInput
        style={styles.input}
        placeholder="Your name"
        placeholderTextColor={Colors.textMuted}
        value={name}
        onChangeText={setName}
      />

      <Text style={styles.fieldLabel}>Your home airport</Text>
      <View style={styles.chipRow}>
        {AIRPORT_OPTIONS.map((code) => (
          <TouchableOpacity
            key={code}
            style={[styles.chip, origin === code && styles.chipSelected]}
            onPress={() => setOrigin(code)}
          >
            <Text style={[styles.chipText, origin === code && styles.chipTextSelected]}>
              {code}
            </Text>
          </TouchableOpacity>
        ))}
      </View>

      {/* Availability */}
      <Text style={styles.sectionLabel}>YOUR AVAILABILITY</Text>
      <TextInput
        style={styles.input}
        placeholder="Earliest departure (YYYY-MM-DD)"
        placeholderTextColor={Colors.textMuted}
        value={earliest}
        onChangeText={setEarliest}
      />
      <TextInput
        style={styles.input}
        placeholder="Latest return (YYYY-MM-DD)"
        placeholderTextColor={Colors.textMuted}
        value={latest}
        onChangeText={setLatest}
      />

      {/* Destination votes */}
      <Text style={styles.sectionLabel}>WHERE WOULD YOU GO?</Text>
      <Text style={styles.fieldLabel}>
        Select all destinations you're happy with
      </Text>
      <View style={styles.chipRow}>
        {AIRPORT_OPTIONS.map((code) => (
          <TouchableOpacity
            key={code}
            style={[styles.chip, votes.includes(code) && styles.chipSelected]}
            onPress={() => toggleVote(code)}
          >
            <Text style={[styles.chipText, votes.includes(code) && styles.chipTextSelected]}>
              {code}
            </Text>
          </TouchableOpacity>
        ))}
      </View>

      <View style={styles.buttonRow}>
        {loading ? (
          <ActivityIndicator color={Colors.primary} />
        ) : (
          <Button title="Join trip" onPress={handleJoin} />
        )}
      </View>

    </ScrollView>
  );
}

const styles = StyleSheet.create({
  scroll: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  container: {
    padding: 24,
    paddingBottom: 48,
  },
  heading: {
    fontSize: 28,
    fontWeight: '700',
    color: Colors.textDark,
    letterSpacing: -0.5,
    marginBottom: 6,
  },
  subheading: {
    fontSize: 15,
    color: Colors.textMuted,
    marginBottom: 8,
    lineHeight: 22,
  },
  sectionLabel: {
    fontSize: 11,
    fontWeight: '700',
    color: Colors.textMuted,
    letterSpacing: 1,
    marginTop: 24,
    marginBottom: 12,
  },
  fieldLabel: {
    fontSize: 13,
    color: Colors.textMuted,
    marginBottom: 10,
  },
  input: {
    backgroundColor: Colors.surface,
    borderWidth: 1,
    borderColor: Colors.border,
    borderRadius: 10,
    padding: 14,
    fontSize: 15,
    color: Colors.textDark,
    marginBottom: 12,
  },
  codeInput: {
    fontSize: 20,
    fontWeight: '600',
    letterSpacing: 2,
    color: Colors.primary,
  },
  chipRow: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
    marginBottom: 12,
  },
  chip: {
    paddingVertical: 8,
    paddingHorizontal: 14,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: Colors.border,
    backgroundColor: Colors.surface,
  },
  chipSelected: {
    backgroundColor: Colors.primary,
    borderColor: Colors.primary,
  },
  chipText: {
    fontSize: 13,
    color: Colors.textDark,
    fontWeight: '500',
  },
  chipTextSelected: {
    color: Colors.white,
  },
  buttonRow: {
    marginTop: 32,
  },
});